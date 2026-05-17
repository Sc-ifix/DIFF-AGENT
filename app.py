"""
Diff Reviewer  -  IBM Bob Hackathon MVP
=======================================

A web tool for developers: paste a public GitHub repo URL (optional) and your
`git diff`, and two AI "agents" running on IBM watsonx (Granite) review it:

  Agent 1  - Reviewer:     bugs, edge cases, repo-aligned improvements
  Agent 2  - Alternatives: 2-3 alternative implementations + tradeoffs

Architecture (deliberately simple, see README):
  - No vector DB, no embeddings, no benchmarking agent.
  - Context = (optional) shallow-cloned file tree + the changed files' content
    + the diff itself. Bounded so it never blows the context window or your
    watsonx credit.
  - "Multi-agent" = a sequential orchestrator making two role-specialised
    LLM calls. A legitimate, defensible design at MVP scope.

You do NOT need to understand this code. Set the keys in .env and run it.
See README.md.
"""

import os
import re
import shutil
import subprocess
import tempfile
import requests
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------------
# Configuration  (set these in the .env file - see .env.example)
# ----------------------------------------------------------------------------
WATSONX_API_KEY    = os.getenv("WATSONX_API_KEY", "").strip()
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "").strip()
WATSONX_REGION     = os.getenv("WATSONX_REGION", "us-south").strip()
WATSONX_MODEL_ID   = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-3-8b-instruct").strip()

IAM_URL  = "https://iam.cloud.ibm.com/identity/token"
CHAT_URL = f"https://{WATSONX_REGION}.ml.cloud.ibm.com/ml/v1/text/chat?version=2024-10-08"

# Safety caps - protect the context window AND your hackathon credit.
MAX_DIFF_CHARS        = 16000
MAX_FILE_CHARS        = 8000
MAX_FILES_FROM_REPO   = 12
MAX_TREE_ENTRIES      = 200
CLONE_TIMEOUT_SECONDS = 60
MAX_OUTPUT_TOKENS     = 1500


# ----------------------------------------------------------------------------
# watsonx helpers
# ----------------------------------------------------------------------------
def get_iam_token() -> str:
    """Exchange the watsonx API key for a short-lived IBM IAM access token."""
    resp = requests.post(
        IAM_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Accept": "application/json"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey",
              "apikey": WATSONX_API_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def call_watsonx(token: str, system_prompt: str, user_prompt: str) -> str:
    """One chat completion against the watsonx Granite model."""
    payload = {
        "model_id": WATSONX_MODEL_ID,
        "project_id": WATSONX_PROJECT_ID,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": MAX_OUTPUT_TOKENS,
        "temperature": 0.2,
    }
    resp = requests.post(
        CHAT_URL,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json",
                 "Accept": "application/json"},
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


# ----------------------------------------------------------------------------
# Repo + diff utilities
# ----------------------------------------------------------------------------
def changed_files_from_diff(diff_text: str):
    """Pull the list of changed file paths out of a unified git diff."""
    files = []
    for m in re.finditer(r"^diff --git a/(\S+) b/(\S+)", diff_text, re.MULTILINE):
        path = m.group(2)
        if path not in files:
            files.append(path)
    return files


def shallow_clone_context(repo_url: str, changed_files):
    """
    Best-effort: shallow-clone the repo to give the model architectural
    context (a trimmed file tree + the full content of the changed files).
    Returns (tree_text, files_text, note). Never raises - degrades gracefully
    so a live demo cannot hard-fail on a bad/private URL.
    """
    repo_url = (repo_url or "").strip()
    if not repo_url:
        return "", "", "No repo URL given - analysing the diff on its own."

    tmp = tempfile.mkdtemp(prefix="diffrev_")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, tmp],
            check=True, capture_output=True, timeout=CLONE_TIMEOUT_SECONDS,
        )
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        return "", "", ("Could not clone that repo (private, invalid, or too "
                         "large) - analysing the diff on its own.")

    try:
        tree = []
        for root, dirs, fnames in os.walk(tmp):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in fnames:
                rel = os.path.relpath(os.path.join(root, f), tmp)
                tree.append(rel)
                if len(tree) >= MAX_TREE_ENTRIES:
                    break
            if len(tree) >= MAX_TREE_ENTRIES:
                break
        tree_text = "\n".join(sorted(tree))

        chunks = []
        for rel in changed_files[:MAX_FILES_FROM_REPO]:
            fp = os.path.join(tmp, rel)
            if os.path.isfile(fp):
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()[:MAX_FILE_CHARS]
                    chunks.append(f"### FILE: {rel}\n```\n{content}\n```")
                except Exception:
                    pass
        files_text = "\n\n".join(chunks)
        return tree_text, files_text, "Repo cloned - architectural context available."
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------------
# The two agents
# ----------------------------------------------------------------------------
REVIEWER_SYSTEM = (
    "You are a senior software engineer doing a focused code review. "
    "You are precise and concrete. You only flag real issues. For each point "
    "give: the problem, why it matters, and the concrete fix. Respect the "
    "existing repository's conventions and architecture - do not suggest a "
    "rewrite of things that work. Use short markdown sections: "
    "Bugs & Risks, Edge Cases, Improvements. Be terse. No filler, no praise."
)

ALTERNATIVES_SYSTEM = (
    "You are a staff engineer proposing alternative implementations for the "
    "changed code only. Give 2-3 distinct approaches. For EACH: a one-line "
    "summary, a short code sketch, and explicit tradeoffs (performance, "
    "readability, scalability, risk). Be opinionated: end with which one you "
    "would ship and why, in one sentence. No filler."
)


def build_review_prompt(tree_text, files_text, diff_text):
    parts = []
    if tree_text:
        parts.append("REPOSITORY FILE TREE (trimmed):\n" + tree_text)
    if files_text:
        parts.append("CHANGED FILES - CURRENT CONTENT IN REPO:\n" + files_text)
    parts.append("THE DEVELOPER'S DIFF / CHANGES TO REVIEW:\n```diff\n"
                 + diff_text + "\n```")
    parts.append("Review the diff in the context above.")
    return "\n\n".join(parts)


def run_pipeline(repo_url, diff_text):
    """Orchestrator: validate -> context -> Reviewer -> Alternatives."""
    diff_text = (diff_text or "").strip()

    if not (WATSONX_API_KEY and WATSONX_PROJECT_ID):
        msg = ("**Setup not complete.** Open the `.env` file and fill in "
               "`WATSONX_API_KEY` and `WATSONX_PROJECT_ID`, then restart. "
               "See README.md.")
        return msg, msg, ""
    if not diff_text:
        msg = ("Paste your changes in the diff box. Tip: run `git diff` in "
               "your terminal and paste the output. (You can also paste a "
               "plain code snippet - it still works.)")
        return msg, msg, ""
    if len(diff_text) > MAX_DIFF_CHARS:
        msg = (f"That diff is {len(diff_text):,} characters - over the "
               f"{MAX_DIFF_CHARS:,} cap. Review a smaller set of changes "
               f"(this also protects your watsonx credit).")
        return msg, msg, ""

    try:
        changed = changed_files_from_diff(diff_text)
        tree_text, files_text, note = shallow_clone_context(repo_url, changed)
        token = get_iam_token()

        review = call_watsonx(
            token, REVIEWER_SYSTEM,
            build_review_prompt(tree_text, files_text, diff_text),
        )
        alternatives = call_watsonx(
            token, ALTERNATIVES_SYSTEM,
            "Here are the changes:\n```diff\n" + diff_text + "\n```",
        )

        status = f"Context: {note}"
        if changed:
            status += f"  |  Changed files detected: {', '.join(changed[:8])}"
            if len(changed) > 8:
                status += f" (+{len(changed) - 8} more)"
        return review, alternatives, status

    except requests.HTTPError as e:
        detail = ""
        try:
            if e.response is not None:
                detail = e.response.json().get("errors", [{}])[0].get("message", "")
            else:
                detail = str(e)
        except Exception:
            detail = str(e)
        err = (f"**watsonx API error.** {detail}\n\nMost common cause: wrong "
               f"`WATSONX_PROJECT_ID`, `WATSONX_REGION`, or a model your "
               f"account can't access. Check README.md.")
        return err, err, ""
    except Exception as e:
        err = f"**Unexpected error:** {e}"
        return err, err, ""


# ----------------------------------------------------------------------------
# UI  -  clean, technical, dark.  (Looks good in a demo video.)
# ----------------------------------------------------------------------------
CSS = """
:root { --bg:#0d1117; --panel:#161b22; --line:#30363d; --accent:#2f9e6e;
        --text:#e6edf3; --muted:#8b949e; }
.gradio-container { background:var(--bg) !important;
  font-family:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace !important; }
#hdr { border-bottom:1px solid var(--line); padding:14px 4px 18px;
  margin-bottom:8px; }
#hdr h1 { color:var(--text); font-size:24px; letter-spacing:.5px; margin:0; }
#hdr h1 span { color:var(--accent); }
#hdr p { color:var(--muted); font-size:13px; margin:6px 0 0; }
.block, .form { background:var(--panel) !important; border-color:var(--line) !important; }
label span { color:var(--muted) !important; font-size:12px !important;
  text-transform:uppercase; letter-spacing:1px; }
textarea, input { background:#0d1117 !important; color:var(--text) !important;
  border-color:var(--line) !important; font-family:'IBM Plex Mono',monospace !important; }
button.primary { background:var(--accent) !important; border:none !important;
  color:#fff !important; font-weight:600 !important; letter-spacing:.5px; }
#status { color:var(--muted); font-size:12px; padding:6px 2px; }
.prose, .prose * { color:var(--text) !important; }
footer { display:none !important; }
"""

with gr.Blocks() as demo:
    # CSS injected inline so it works on every Gradio version (no fragile
    # css=/title= kwargs that move between releases).
    gr.HTML(
        f"<style>{CSS}</style>"
        '<div id="hdr"><h1>Diff <span>Reviewer</span></h1>'
        '<p>Two AI agents on IBM watsonx review your changes in the context '
        'of the whole repo &mdash; bugs, edge cases, and alternative '
        'implementations.</p></div>'
    )
    with gr.Row():
        with gr.Column(scale=1):
            repo_in = gr.Textbox(
                label="GitHub repo URL  (optional - gives the AI context)",
                placeholder="https://github.com/owner/repo",
            )
            diff_in = gr.Textbox(
                label="Your git diff  (run: git diff)",
                placeholder="Paste the output of `git diff` here.\n"
                            "No diff? Paste a code snippet instead.",
                lines=18,
            )
            go = gr.Button("Review my changes", variant="primary")
            status = gr.Markdown(elem_id="status")
        with gr.Column(scale=1):
            with gr.Tab("Agent 1 — Review"):
                review_out = gr.Markdown()
            with gr.Tab("Agent 2 — Alternatives"):
                alt_out = gr.Markdown()

    go.click(
        fn=run_pipeline,
        inputs=[repo_in, diff_in],
        outputs=[review_out, alt_out, status],
    )

if __name__ == "__main__":
    # share=True gives you a PUBLIC link - use it in your demo video / submission.
    demo.launch(share=True)
