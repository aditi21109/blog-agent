# Blog Studio — your first small agent

Python + Gradio + Groq. The model creates an outline, writes a draft, reviews it, and decides whether to revise it once.

## Run on Windows

Open a terminal in this folder, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and replace the placeholder with your Groq key. Keep it private.

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the local URL shown in the terminal if your browser does not open automatically. Stop the app with Ctrl+C.

## How to learn from this

1. Read `agent.py`: `ask()` is the shared model-call function.
2. Follow the outline and draft steps: these form a fixed workflow.
3. Inspect the review JSON: `needs_revision` controls the next action.
4. Follow the conditional revision: this is the small decision loop.
5. Read `app.py`: it adds controls, progress, and Markdown downloads.

This is a bounded agentic workflow, not an autonomous research agent. It uses three calls normally and four if revision is requested. No agent framework is needed.

The default is `qwen/qwen3.8-27b` (check the model card for its license). Change `GROQ_MODEL` in `.env` to another model supporting chat and JSON mode if needed. Open weights and open source are not interchangeable terms.

Groq's free plan has usage limits; available models and account limits can change. Check https://console.groq.com/docs/models and https://console.groq.com/docs/rate-limits.

Editorial review checks writing quality; it does not establish factual accuracy. No search or external sources are used. Blogs are saved in `blogs/`; delete old drafts when no longer needed.
