**User:**

<task>
1. Product Concept

We are building a tool that integrates with GitHub repositories.

Core Workflow:
User pastes or connects a GitHub repository
System performs full repository analysis (code structure, patterns, quality, architecture, issues)
While the developer is working on staged/uncommitted changes, they submit or sync their current code into the system
A set of AI agents analyze the changes in context of the entire repository
Core Outputs:
Code improvement suggestions
Bug detection and edge-case analysis
2–3 alternative implementation strategies
Refactoring suggestions aligned with existing repo style and architecture
2. Multi-Agent System

Design the system assuming multiple specialized agents, including but not limited to:

A. Repo Understanding Agent
Builds structural understanding of the repository
Extracts architecture, dependencies, coding patterns
B. Change Analysis Agent
Compares staged changes vs existing codebase
Identifies risks, inconsistencies, and improvements
C. Alternative Solutions Agent
Generates multiple implementation approaches (2–3)
Evaluates tradeoffs (performance, readability, scalability)
D. Benchmarking Agent (Advanced)
Finds similar GitHub repositories
Compares quality, structure, and implementation differences
Extracts best practices from higher-quality repos
E. Feedback/Issue Agent (Optional)
If available, analyzes GitHub issues/comments/PR feedback
Converts feedback into actionable code changes
3. What I want from you

Provide a structured, engineering-grade response covering:

(1) Feasibility Analysis
Is this system realistic with current LLM + tooling?
What parts are easy vs hard vs research-level?
(2) System Architecture
End-to-end pipeline design
How agents communicate (orchestrator vs swarm vs graph)
Data flow between repo, embeddings, and agents
(3) Implementation Plan
Step-by-step MVP build strategy
Suggested tech stack (LLMs, vector DB, GitHub API, etc.)
How to integrate into developer workflow (CLI, VSCode, web app, etc.)
(4) Time & Resource Estimation
Solo developer vs small team
MVP vs production-grade system
(5) Risks & Bottlenecks
Scaling issues
Cost of analysis
Latency problems
Context window limitations
GitHub API constraints
(6) Improvements / Simplifications
Suggest a simpler MVP version that still delivers high value
Suggest features that should be removed or deferred
4. Output Requirements
Be highly structured and technical
Avoid vague or motivational language
Prioritize system design clarity over ideation
Assume I am building this seriously, not just brainstorming

If you want, I can also 
compress this into a one-paragraph “ultra-dense prompt” that gets even sharper outputs, or 
turn it into a YC-style product spec.

tell it also what not to do and set an identit for it

Here’s a fully prompt-engineered version with (1) a strong identity, (2) clear boundaries, and (3) explicit “do not do” constraints to keep Claude focused and non-generic.

Ultra-Refined Prompt (Claude Pro – System Design Agent)

You are a principal-level AI systems architect at a top-tier AI lab, with deep experience in:

multi-agent systems
code intelligence tools (like GitHub Copilot, Sourcegraph, etc.)
distributed LLM architectures
developer tooling and CI/CD systems

You think in system design diagrams, pipelines, tradeoffs, and production constraints.
You do NOT respond like a chatbot—you respond like an engineering design reviewer.

🚫 Hard Constraints (Do NOT do this)
Do NOT give vague brainstorming answers
Do NOT be motivational or use filler language
Do NOT oversimplify architecture unless explicitly asked
Do NOT ignore scaling, cost, latency, or context window issues
Do NOT assume infinite compute or perfect LLMs
Do NOT skip failure cases or edge cases
Do NOT present ideas without explaining feasibility tradeoffs
Do NOT stay surface-level (no “this is a great idea” type responses)
🧠 Product Idea to Evaluate

We are building an AI-powered developer tool integrated with GitHub.

Core Workflow:
User connects or pastes a GitHub repository
System analyzes the entire repo:
structure
architecture
code patterns
dependencies
quality issues
While the developer is working on staged/uncommitted code:
they submit/sync changes to the system
AI agents analyze the changes in context of the full repository
Core Outputs:
Code improvement suggestions
Bug detection + edge-case identification
2–3 alternative implementations
Refactoring suggestions aligned with repo style
🤖 Multi-Agent System (Required Design)

You MUST design a multi-agent architecture including:

1. Repository Intelligence Agent

Builds a structural + semantic map of the repository

2. Change Impact Agent

Analyzes staged diffs vs repo context and predicts issues

3. Solution Generator Agent

Produces multiple implementation alternatives (2–3)

4. Benchmarking Agent (Advanced)
Finds similar GitHub repos
Compares design quality and patterns
Extracts best practices from superior implementations
5. Feedback Mining Agent (Optional)
Reads GitHub issues / PR comments
Converts feedback into actionable engineering changes
📌 Your Tasks

Provide a highly structured engineering response covering:

(1) Feasibility Analysis
What parts are realistic today vs hard vs research-level?
Where LLMs will fail or hallucinate in this system
(2) System Architecture
Full end-to-end design
Agent orchestration model (graph, pipeline, swarm, or hybrid)
Data flow between:
GitHub
embeddings/vector DB
LLM agents
diff analyzer

Include reasoning for architecture choice.

(3) Implementation Plan (MVP → Production)
Step-by-step MVP plan (minimum viable system)
Tools/stack (GitHub API, vector DB, LLMs, etc.)
Integration strategy (CLI / VSCode extension / web app)
How to process repo efficiently under token limits
(4) Time & Resource Estimate
Solo developer vs small team
MVP timeline vs production-grade timeline
Cost considerations (LLM API usage, embeddings, storage)
(5) Risks & Bottlenecks

You MUST explicitly analyze:

context window limitations
repo scaling issues (large monorepos)
latency in multi-agent systems
cost explosion risk
GitHub API rate limits
hallucination in “benchmarking agent”
(6) Simplification Strategy
What to cut to make this buildable in 1–2 weeks
What features are “nice but dangerous”
A minimal high-impact version of this product
🎯 Output Style Requirements
Be structured like a technical design doc
Use clear headings and hierarchy
Be precise and opinionated where needed
Prefer correctness over optimism
Think like you are reviewing this for engineering approval
</task>
<environment_details>
# VSCode Visible Files
../../../../Untitled-1

# VSCode Open Tabs
../../../../Untitled-1

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T16:29:40.735Z
User time zone: Asia/Dubai, UTC+4:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>


# Current Workspace Directory (/Users/hfk/Desktop/IBM BOB) Files
No files found.
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze this GitHub-integrated AI code review system from a principal systems architect perspective. Let me start by gathering some context about your current development environment and then break down this complex system design.

<read_file>
<args>
  <file>
    <path>../../../../Untitled-1</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for '../../../../Untitled-1'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>../../../../Untitled-1</path><error>File not found</error><notice>The file was not found. Consider using list_files to find available files before attempting to read them.</notice></file>
</files>
<environment_details>
# VSCode Visible Files
../../../../Untitled-1

# VSCode Open Tabs
../../../../Untitled-1

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T16:29:44.157Z
User time zone: Asia/Dubai, UTC+4:00

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<ask_followup_question>
<question>Before I create the comprehensive system design, I need to clarify a few critical constraints that will significantly impact the architecture:

1. **Target Scale**: What repository sizes are you targeting? (Small: <10K files, Medium: 10K-50K files, Large: 50K+ files like Linux kernel)

2. **Latency Requirements**: What's acceptable analysis time? (Real-time: <5s, Interactive: 5-30s, Batch: minutes)

3. **Budget Constraints**: What's your monthly budget for LLM API calls and infrastructure? (Bootstrapped: <$100/mo, Funded: $1K-10K/mo, Enterprise: >$10K/mo)

4. **Primary Integration Point**: Where should this live initially?</question>
<follow_up>
<suggest>Medium repos (10K-50K files), Interactive latency (5-30s), Bootstrapped budget (<$100/mo), VSCode extension</suggest>
<suggest>Small repos (<10K files), Real-time latency (<5s), Funded budget ($1K-10K/mo), CLI tool</suggest>
<suggest>All sizes, Batch processing (minutes), Funded budget ($1K-10K/mo), Web application</suggest>
<suggest>Skip constraints - design for ideal case and I'll adapt later</suggest>
</follow_up>
</ask_followup_question>

---

**User:**

[ask_followup_question for 'Before I create the comprehensive system design, I need to clarify a few critical constraints that will significantly impact the architecture:

1. **Target Scale**: What repository sizes are you targeting? (Small: <10K files, Medium: 10K-50K files, Large: 50K+ files like Linux kernel)

2. **Latency Requirements**: What's acceptable analysis time? (Real-time: <5s, Interactive: 5-30s, Batch: minutes)

3. **Budget Constraints**: What's your monthly budget for LLM API calls and infrastructure? (Bootstrapped: <$100/mo, Funded: $1K-10K/mo, Enterprise: >$10K/mo)

4. **Primary Integration Point**: Where should this live initially?'] Result:
The tool execution failed with the following error:
<error>
Error parsing ask_followup_question args: {"name":"Error","message":"Failed to parse ask_followup_question parameters: Failed to parse follow_up XML: Failed to parse XML: Unexpected end of suggest","stack":"Error: Failed to parse ask_followup_question parameters: Failed to parse follow_up XML: Failed to parse XML: Unexpected end of suggest\n\tat fvr.handle (/Applications/IBM Bob.app/Contents/Resources/app/extensions/bob-code/dist/extension.js:6072:798)\n\tat sZ (/Applications/IBM Bob.app/Contents/Resources/app/extensions/bob-code/dist/extension.js:7086:3634)\n\tat process.processTicksAndRejections (node:internal/process/task_queues:105:5)"}
</error>
[ask_followup_question for 'Before I create the comprehensive system design, I need to clarify a few critical constraints that will significantly impact the architecture:

1. **Target Scale**: What repository sizes are you targeting? (Small: <10K files, Medium: 10K-50K files, Large: 50K+ files like Linux kernel)

2. **Latency Requirements**: What's acceptable analysis time? (Real-time: <5s, Interactive: 5-30s, Batch: minutes)

3. **Budget Constraints**: What's your monthly budget for LLM API calls and infrastructure? (Bootstrapped: <$100/mo, Funded: $1K-10K/mo, Enterprise: >$10K/mo)

4. **Primary Integration Point**: Where should this live initially?'] Result:
<error>Failed to parse ask_followup_question parameters: Failed to parse follow_up XML: Failed to parse XML: Unexpected end of suggest</error>
<environment_details>
# VSCode Visible Files
../../../../Untitled-1

# VSCode Open Tabs
../../../../Untitled-1

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T16:29:52.173Z
User time zone: Asia/Dubai, UTC+4:00

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<ask_followup_question>
<question>Before I create the comprehensive system design, I need to clarify a few critical constraints that will significantly impact the architecture:

1. Target Scale: What repository sizes are you targeting?
2. Latency Requirements: What is acceptable analysis time?
3. Budget Constraints: What is your monthly budget for LLM API calls and infrastructure?
4. Primary Integration Point: Where should this live initially?</question>
<follow_up>
<suggest>Medium repos 10K-50K files, Interactive latency 5-30s, Bootstrapped budget under $100/mo, VSCode extension</suggest>
<suggest>Small repos under 10K files, Real-time latency under 5s, Funded budget $1K-10K/mo, CLI tool</suggest>
<suggest>All sizes, Batch processing minutes, Funded budget $1K-10K/mo, Web application</suggest>
<suggest>Skip constraints - design for ideal case and I will adapt later</suggest>
</follow_up>
</ask_followup_question>

