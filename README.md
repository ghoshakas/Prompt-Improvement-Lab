# Prompt Improvement Lab

> A hands-on tool that proves *how much the wording of a prompt matters*. Pick a
> task, run a lazily-written prompt and a carefully engineered one on the **same
> input** through Google's Gemini models, and watch the two answers appear side
> by side — with a plain-English explanation of why the better prompt wins.

---

## Table of contents

1. [The problem this solves](#1-the-problem-this-solves)
2. [What the app does](#2-what-the-app-does)
3. [Why it's useful / who it helps](#3-why-its-useful--who-it-helps)
4. [The five tasks](#4-the-five-tasks)
5. [Architecture](#5-architecture)
6. [Tech stack](#6-tech-stack)
7. [Project structure](#7-project-structure)
8. [Getting started](#8-getting-started)
9. [Configuration](#9-configuration)
10. [API reference](#10-api-reference)
11. [How a prompt gets "improved"](#11-how-a-prompt-gets-improved)
12. [Extending the lab](#12-extending-the-lab)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. The problem this solves

Large language models are only as good as the instructions you give them. Most
people type the first thing that comes to mind — *"summarize this"*, *"make it
better"*, *"get the important info"* — and then get frustrated when the model
replies with the wrong length, an inconsistent format, invented facts, or a tone
that doesn't fit.

The fix is almost never a bigger model. It's a **better prompt**: one that states
the role, the context, the constraints, and the exact output format. The trouble
is that this lesson is hard to *feel* from reading about it. You have to see the
before and after, on the same input, to believe how big the difference is.

**Prompt Improvement Lab makes that difference visible and interactive.**

## 2. What the app does

For each of five everyday LLM tasks, the app lets you:

1. **Select a task** — summarization, classification, extraction, rewriting, or content generation.
2. **See both prompts** — the lazy "original" and the engineered "improved" version, so you can inspect exactly what changed.
3. **Edit the input** — start from a built-in sample or paste your own text.
4. **Run the comparison** — both prompts are sent to Gemini against the identical input, in parallel.
5. **Compare the outputs** — the two responses render side by side, each with its response time.
6. **Understand why** — a short, bulleted explanation spells out *why* the improved prompt produces a more useful, consistent, and structured result.

Everything runs live against the Gemini API, so the outputs are real, not canned.

## 3. Why it's useful / who it helps

- **Learners & students** — a concrete, interactive way to learn prompt engineering instead of reading theory.
- **Developers integrating LLMs** — a sandbox to see how structure (schemas, enums, explicit formats) turns flaky output into something you can safely parse in code.
- **Writers, analysts, support teams** — anyone who uses AI tools daily and wants more reliable results from them.
- **Teachers & demos** — the side-by-side layout makes the point in seconds, which is perfect for a workshop or presentation.

The broader payoff: better prompts mean **fewer retries, lower token cost,
output you can trust, and results that are consistent run after run** — the
difference between a toy and a dependable tool.

## 4. The five tasks

| Task | Lazy prompt (original) | What the improved prompt adds | Why it's better |
|------|------------------------|-------------------------------|-----------------|
| **Summarization** | "Summarize this: …" | Editor role, fixed length (3 bullets, <20 words each), keep all numbers, add nothing new | Predictable length & format; no dropped or invented facts |
| **Classification** | "What category is this? …" | Fixed label set, pick exactly one, JSON output with `label` / `confidence` / `reason`, "unknown" escape hatch | Parseable, consistent labels instead of ad-hoc categories |
| **Extraction** | "Get the important info from this: …" | Explicit JSON schema, `null` for missing fields, ISO dates, "don't guess" | Machine-readable output with no hallucinated values |
| **Rewriting** | "Make this better: …" | Target audience & tone, preserve meaning & length, return only the rewrite | "Better" gets a direction; original intent is preserved |
| **Content generation** | "Write something about: …" | Role, format, length, audience, tone, must-include points, call to action | Usable, on-brand copy instead of generic filler |

The prompts and explanations live in [`backend/prompts.py`](backend/prompts.py) — one place to read or edit them all.

## 5. Architecture

The app is deliberately split into two small, independent pieces that talk over
HTTP. The **API key never leaves the backend**, so it is never exposed to the
browser.

```
                            ┌──────────────────────────────────────────────┐
                            │                   BROWSER                      │
                            │                                                │
   ┌────────────────────────────────────────────────────────────────┐       │
   │  React + Vite + Tailwind  (frontend/, dev server on :5173)       │       │
   │                                                                  │       │
   │   App.tsx  ── state: active task, input text, two output panels  │       │
   │     │                                                            │       │
   │     ├─ TaskSelector   (choose one of the 5 tasks)                │       │
   │     ├─ PromptCard x2   (show original vs improved prompt)        │       │
   │     ├─ OutputPanel x2  (side-by-side results + latency)          │       │
   │     └─ ExplanationCard (why the improved prompt wins)            │       │
   │                                                                  │       │
   │   api.ts  ── fetch wrappers around the two endpoints             │       │
   └───────────────────────────────┬──────────────────────────────────┘      │
                            └───────┼────────────────────────────────────────┘
                                    │  HTTP (JSON)   GET /api/tasks
                                    │                POST /api/run
                                    ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  FastAPI backend  (backend/, server on :8000)                      │
   │                                                                    │
   │   app.py           ── routes + CORS; fills {input} into a prompt   │
   │     │                                                              │
   │     ├─ prompts.py        ── the 5 task definitions (data)          │
   │     ├─ config.py         ── all settings (model, timeout, ports)   │
   │     └─ gemini_client.py  ── the ONLY module that calls Gemini      │
   └───────────────────────────────┬────────────────────────────────────┘
                                    │  Google GenAI SDK (google-genai)
                                    ▼
                         ┌────────────────────────┐
                         │   Gemini API (Google)   │
                         │   model: gemini-3.x     │
                         └────────────────────────┘
```

### Request flow (clicking "Run comparison")

1. On load, the frontend calls `GET /api/tasks` and caches the five task definitions (prompts, sample input, explanation).
2. When you click **Run comparison**, `App.tsx` fires **two** `POST /api/run` calls in parallel — one with `variant: "original"`, one with `variant: "improved"` — both carrying the same input text.
3. For each call, `app.py` looks up the task, injects your input into that prompt template, and hands the final prompt to `gemini_client.generate()`.
4. `gemini_client.py` calls the Gemini API (with a bounded timeout and retries), and returns the text.
5. The backend responds with `{ output, model, latency_ms }`; the two panels render as soon as each arrives.

### Design principles

- **Single responsibility per module.** `prompts.py` is data, `config.py` is settings, `gemini_client.py` is the only thing that knows about Gemini, `app.py` is just wiring. Swapping models or even providers touches exactly one file.
- **Secrets stay server-side.** The browser only ever talks to your own backend.
- **Data-driven tasks.** Adding a sixth task is a dict entry, not new code.
- **Fail friendly.** Missing key, a busy model, or a down backend each produce a clear message in the UI, never a blank screen.

## 6. Tech stack

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend framework | **React 18 + TypeScript** | Component model fits the compare UI; types catch mistakes early |
| Build tool | **Vite 5** | Instant dev server and fast builds |
| Styling | **Tailwind CSS v4** | Clean, responsive UI without hand-written CSS |
| Backend framework | **FastAPI** | Tiny, typed, automatic request validation + OpenAPI docs |
| Server | **Uvicorn** | Standard ASGI server for FastAPI |
| LLM SDK | **google-genai** | Google's current Gemini SDK |
| Config | **python-dotenv** | Keeps secrets in `.env`, out of source control |

## 7. Project structure

```
ip/
├─ backend/
│  ├─ app.py             # FastAPI app: the two routes + CORS + entry point
│  ├─ config.py          # ALL settings in one place (model, timeout, ports, origins)
│  ├─ gemini_client.py   # the only module that talks to Gemini
│  ├─ prompts.py         # the 5 tasks: original + improved prompt, sample, explanation
│  ├─ requirements.txt   # Python dependencies
│  ├─ .env.example       # template — copy to .env and add your key
│  └─ .env               # your real GEMINI_API_KEY (git-ignored)
│
├─ frontend/
│  ├─ src/
│  │  ├─ App.tsx         # the compare screen + state
│  │  ├─ api.ts          # calls to /api/tasks and /api/run
│  │  ├─ types.ts        # shared TypeScript types
│  │  └─ components/
│  │     ├─ TaskSelector.tsx     # the 5 task tabs
│  │     ├─ PromptCard.tsx       # collapsible original/improved prompt
│  │     ├─ OutputPanel.tsx      # one result panel (loading/error/output)
│  │     └─ ExplanationCard.tsx  # the "why it's better" bullets
│  ├─ index.html
│  ├─ package.json
│  └─ vite.config.ts
│
├─ setup.ps1 / setup.bat  # one-time: install everything
├─ run.ps1   / run.bat    # start backend + frontend together
├─ .gitignore
└─ README.md              # this file
```

## 8. Getting started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- A **Gemini API key** — free from <https://aistudio.google.com/apikey>

### Option A — the easy way (Windows)

```powershell
# 1. one-time install (creates the venv, installs backend + frontend deps)
.\setup.ps1

# 2. put your key in backend\.env  (setup.ps1 creates the file for you)
#    GEMINI_API_KEY=your-key-here

# 3. start both servers and open the browser
.\run.ps1
```

Or just double-click **`setup.bat`** once, then **`run.bat`** whenever you want to use it.

### Option B — manual (any OS)

**Backend** (terminal 1):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env          # then edit .env and add GEMINI_API_KEY
python app.py                 # serves on http://localhost:8000
```

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev                   # serves on http://localhost:5173
```

Open **http://localhost:5173** and start comparing.

## 9. Configuration

Everything configurable lives in [`backend/config.py`](backend/config.py); each
value can be overridden by an environment variable in `backend/.env`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `GEMINI_API_KEY` | — (required) | Your Gemini API key |
| `GEMINI_MODEL` | `gemini-3.6-flash` | Which model to call |
| `GEMINI_TIMEOUT_MS` | `30000` | Per-request timeout |
| `GEMINI_RETRIES` | `3` | Retries for transient "high demand" errors |
| `HOST` | `127.0.0.1` | Backend bind address |
| `PORT` | `8000` | Backend port |
| `ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Browsers allowed to call the API |

Frontend only: `VITE_API_BASE` (in `frontend/.env`) points the UI at a backend
somewhere other than `http://localhost:8000`.

> **Note on models:** Google rotates model names over time, and newer flash
> models are sometimes temporarily overloaded. If you see a "model is busy"
> message, retry, or set a different `GEMINI_MODEL` (e.g. `gemini-3.5-flash`) —
> no code change needed.

## 10. API reference

### `GET /api/tasks`

Returns all five task definitions.

```json
[
  {
    "id": "summarization",
    "name": "Summarization",
    "description": "Condense a long passage into a short, faithful summary.",
    "sample_input": "…",
    "original_prompt": "Summarize this:\n\n{input}",
    "improved_prompt": "You are an experienced business editor…{input}",
    "explanation": ["…", "…"]
  }
]
```

### `POST /api/run`

Runs one prompt variant against one input.

**Request**

```json
{ "task_id": "summarization", "variant": "improved", "input": "your text here" }
```

**Response**

```json
{ "output": "• Revenue: $4.2M, up 18%…", "model": "gemini-3.6-flash", "latency_ms": 1342 }
```

Errors come back with a helpful `detail` message and an appropriate status code
(`400` for a missing key, `404` for an unknown task, `502` for an upstream
Gemini failure).

Interactive API docs are available at **http://localhost:8000/docs** while the
backend is running (FastAPI generates them automatically).

## 11. How a prompt gets "improved"

Every improved prompt in this project applies the same repeatable recipe:

1. **Role** — tell the model who it is ("You are an experienced editor").
2. **Context** — what the input is and what it's for.
3. **Explicit constraints** — length, what to keep, what to avoid.
4. **Output format** — bullets, JSON schema, "return only the rewrite", etc.
5. **Edge-case handling** — "use null if missing", "use 'unknown' if unclear", "don't guess".

That structure is what turns a vague request into output that is **useful**
(it answers the real need), **consistent** (same shape every run), and
**structured** (parseable / ready to use). The app is essentially a live
demonstration of this recipe across five task types.

## 12. Extending the lab

- **Add a task:** append one dict to `TASKS` in `backend/prompts.py` with an `id`, `name`, `description`, `sample_input`, `original_prompt`, `improved_prompt`, and `explanation`. The UI picks it up automatically — no frontend change needed.
- **Change a model:** set `GEMINI_MODEL` in `backend/.env`.
- **Swap providers:** reimplement `gemini_client.generate()`; nothing else needs to change.
- **Tune a prompt:** edit the `improved_prompt` string and re-run — the comparison updates instantly.

## 13. Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| UI shows *"Can't reach the backend"* | The FastAPI server isn't running. Start it (`python app.py` in `backend/`). |
| *"GEMINI_API_KEY is not set"* | Create `backend/.env` from `.env.example` and paste your key. |
| *"model is busy / high demand"* (502) | Transient Gemini capacity issue. Retry, or set a different `GEMINI_MODEL`. |
| *"model … is no longer available"* (404) | That model was retired for your key. Set a current one in `GEMINI_MODEL`. |
| Frontend loads but calls fail with CORS errors | Make sure the frontend origin is in `ALLOWED_ORIGINS` and the backend is on port 8000. |

---
