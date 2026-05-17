---
title: IBM Hackathon Submission
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Diff Reviewer

Two AI agents running on **IBM watsonx (Granite)** review your code changes in
the context of the whole repository: bugs, edge cases, repo-aligned
improvements, and 2–3 alternative implementations with tradeoffs.

Built for the **IBM Bob Hackathon**. A tool developers would actually use.
One Python file. No separate servers, no frontend build, no database.

---

## ⚠️ READ THIS FIRST — submission requirement

This hackathon requires:

1. Your code on a **public GitHub repo**.
2. An **exported IBM Bob session report** showing Bob helped build it.
3. Judging weighs **creative use of IBM Bob** heavily.

So: do a meaningful part of the build **inside IBM Bob** (not only Cursor),
and export the Bob report before you submit. Skipping the Bob report can get
you disqualified no matter how good the project is. Don't leave it to the end.

---

## Setup (≈10 minutes, no coding needed)

You do **not** need to know Python. You run two commands and paste keys.

### 1. Install Python (if needed)
Python 3.10+ from <https://www.python.org/downloads/>. On Windows, tick
**"Add Python to PATH"** during install.

### 2. Install dependencies
Open a terminal **in this folder** and run:

```
pip install -r requirements.txt
```

### 3. Add your watsonx keys
Copy the template, then fill it in:

- Mac/Linux: `cp .env.example .env`
- Windows: `copy .env.example .env`

Open the new `.env` file in any text editor and paste your real values:

| Variable | Where to get it |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud → Manage → Access (IAM) → API keys → **Create** |
| `WATSONX_PROJECT_ID` | watsonx.ai project → **Manage** tab → General → Project ID |
| `WATSONX_REGION` | Region of your watsonx instance (`us-south`, `eu-de`, …) |
| `WATSONX_MODEL_ID` | Leave default unless the app says the model is unavailable |

### 4. Run it
```
python app.py
```

It prints two links. The **public** one (ends in `gradio.live`) works from any
browser — use that one in your **demo video** and submission.

---

## How to demo it (for the video)

1. Pick any small public GitHub repo. Paste its URL in the top box.
2. In a clone of that repo, make a small change, run `git diff`, copy the
   output, paste it in the diff box.
   *(No repo handy? Paste any code snippet in the diff box — it still works.)*
3. Click **Review my changes**. Show the **Review** tab, then the
   **Alternatives** tab. ~10–30 seconds per run.

Keep the video under ~2 minutes: problem → live run → the two outputs.

---

## Architecture (for judges / your write-up)

A deliberately scoped MVP. "Multi-agent" = a **sequential orchestrator**
making two **role-specialised** watsonx calls:

```
repo URL + git diff
   → shallow clone (depth 1) for file-tree + changed-file context  [optional]
   → Agent 1  "Reviewer"      : bugs, edge cases, repo-aligned fixes
   → Agent 2  "Alternatives"  : 2–3 implementations + tradeoffs
   → results in the UI
```

**Deliberately cut, and why** (so the build is finishable and reliable):

- *Embeddings / vector DB* — unnecessary; context is bounded to changed files
  + tree, which fits the model window directly.
- *Benchmarking agent* (rank similar repos) — highest hallucination risk, no
  reliable demo value.
- *Feedback/issue mining* — low reliability, deferred.
- *Live git daemon for staged changes* — replaced by "paste your `git diff`",
  keeping it a web app with zero install for the end user.

Every input is size-capped (`MAX_*` in `app.py`) so a runaway test cannot
blow the context window or your hackathon credit.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Setup not complete" | `.env` missing or keys blank. Redo step 3, restart. |
| "watsonx API error" | Usually wrong `WATSONX_PROJECT_ID` / `WATSONX_REGION`, or model not enabled for your account. |
| Clone note: "could not clone" | Repo private/invalid/huge. It still reviews the diff alone — fine for the demo. |
| `pip` not found | Python not installed or not on PATH (reinstall, tick "Add to PATH"). |
