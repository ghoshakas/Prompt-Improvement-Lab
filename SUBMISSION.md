# Prompt Improvement Lab — Project Submission

*Redesigning weak prompts into reliable, structured instructions.*

---

## 1. Project Overview

Prompt Improvement Lab is a small full-stack web application that demonstrates,
interactively, how much the **wording of a prompt** affects the quality of a
large language model's output. For each of five common tasks it places a poorly
written *"original"* prompt next to a carefully engineered *"improved"* one, runs
both on the **same input** through Google's Gemini API, and shows the two results
side by side — along with a short explanation of why the improved prompt produces
a more useful, consistent, and structured result.

The project satisfies the brief: build an application where a user can select a
task, run the original prompt, run an improved prompt, compare the outputs, and
understand why the improved prompt is better, across at least five tasks.

## 2. The Problem and Why It Matters

Large language models are only as good as the instructions they are given. In
everyday use, people type the first thing that comes to mind — *"summarize this"*,
*"make it better"*, *"get the important info"* — and are then disappointed when
the model returns the wrong length, an inconsistent format, invented facts, or an
unsuitable tone.

The remedy is rarely a bigger or more expensive model; it is a **better prompt** —
one that specifies the role, the context, the constraints, and the exact output
format. The difficulty is that this lesson is hard to appreciate in the abstract.
People need to see the before and after, on the same input, to believe how large
the difference really is.

**This application makes that difference visible and interactive.** The practical
payoff of better prompting is concrete: fewer retries, lower token cost, output
that can be trusted, and results that are consistent from one run to the next —
the difference between a novelty and a dependable tool.

## 3. Objectives and How the Brief Is Met

| Requirement | How it is met |
|-------------|---------------|
| Select a task | Five tasks are shown as tabs; selecting one loads its prompts, a sample input, and its explanation. |
| Run the original prompt | The lazy prompt is sent to Gemini against the current input via the backend. |
| Run the improved prompt | The engineered prompt is sent against the identical input, in parallel with the original. |
| Compare the outputs | The two responses render in side-by-side panels, each with its response time. |
| Explain why it is better | An explanation card lists the concrete reasons the improved prompt wins for that task. |
| At least five tasks | Summarization, classification, extraction, rewriting, and content generation are all included. |

## 4. What Was Built

The application is a two-part system: a **React single-page front end** for the
comparison experience, and a **Python (FastAPI) back end** that holds the task
definitions and is the only component that talks to the Gemini API. Key features:

- A task selector for the five supported tasks.
- An editable input box, pre-filled with a realistic sample so the tool is useful immediately but open to the user's own text.
- Collapsible prompt cards that reveal the exact original and improved prompt text, so the user can see precisely what changed.
- A single **"Run comparison"** action that fires both prompts at once and streams each result into its own panel with a loading state and latency readout.
- An explanation card that articulates, per task, why the improved prompt is superior.
- Friendly, inline error handling for a missing API key, a busy model, or an unreachable backend — never a blank screen.

## 5. The Five Tasks

Every improved prompt is deliberately contrasted with the kind of lazy prompt
people actually write.

| Task | Original (lazy) | Improved prompt adds | Why it is better |
|------|-----------------|----------------------|------------------|
| **Summarization** | "Summarize this: …" | Editor role; exactly 3 bullets under 20 words; keep all numbers; add nothing new | Predictable length and format; no dropped or invented facts |
| **Classification** | "What category is this? …" | Fixed label set; pick one; JSON with label, confidence, reason; "unknown" option | Parseable, consistent labels instead of ad-hoc categories |
| **Extraction** | "Get the important info …" | Explicit JSON schema; null for missing; ISO dates; "don't guess" | Machine-readable output with no hallucinated values |
| **Rewriting** | "Make this better: …" | Target audience and tone; preserve meaning and length; return only the rewrite | "Better" is given a direction; original intent is preserved |
| **Content generation** | "Write something about …" | Role, format, length, audience, tone, must-include points, call to action | Usable, on-brand copy instead of generic filler |

## 6. Architecture

The system is split into two small, independent services that communicate over
HTTP in JSON. A central design rule is that the **Gemini API key never leaves the
back end**, so it is never exposed to the browser.

```
Browser  ─────▶  React UI (Vite, :5173)
   TaskSelector | PromptCard ×2 | OutputPanel ×2 | ExplanationCard
            │  HTTP / JSON
            │  GET /api/tasks     POST /api/run
            ▼
FastAPI back end (:8000)
   app.py  ─▶  prompts.py (data) + config.py (settings)
   app.py  ─▶  gemini_client.py   (the only caller of Gemini)
            │  google-genai SDK
            ▼
Gemini API (Google)   model: gemini-3.6-flash
```

### Components

- **Front end** (React + Vite + Tailwind, port 5173): the user interface. `App.tsx` holds the state — the active task, the input text, and the two output panels — and composes the `TaskSelector`, `PromptCard`, `OutputPanel`, and `ExplanationCard` components. A small `api.ts` module wraps the two backend calls.
- **Back end** (FastAPI, port 8000): exposes two endpoints and performs prompt assembly. `app.py` is the wiring; `prompts.py` holds the five task definitions as data; `config.py` centralises every setting; `gemini_client.py` is the single module that calls Gemini.
- **Gemini API** (Google): the language model that produces both outputs, reached through the official `google-genai` SDK.

### Request flow when the user clicks "Run comparison"

1. On load, the front end calls `GET /api/tasks` and caches the five task definitions.
2. On the click, the front end fires two `POST /api/run` calls in parallel — one with variant `"original"`, one with `"improved"` — both carrying the same input text.
3. For each call, the back end looks up the task, injects the input into that prompt template, and passes the final prompt to the Gemini client.
4. The Gemini client calls the API with a bounded timeout and automatic retries, and returns the text.
5. The back end responds with the output, the model name, and the latency; each panel renders as soon as its result arrives.

### Design principles

- **Single responsibility per module:** data, settings, Gemini access, and wiring are each isolated, so changing the model — or even the provider — touches exactly one file.
- **Secrets stay server-side:** the browser only ever talks to the project's own back end.
- **Data-driven tasks:** adding a sixth task is a single dictionary entry, with no front-end change.
- **Fail friendly:** every error path yields a clear, human-readable message in the UI.

## 7. Technology Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Front-end framework | React 18 + TypeScript | Component model fits the compare UI; types catch mistakes early |
| Build tool | Vite 5 | Instant dev server and fast production builds |
| Styling | Tailwind CSS v4 | Clean, responsive UI without hand-written CSS |
| Back-end framework | FastAPI | Small, typed, automatic validation and OpenAPI docs |
| Server | Uvicorn | Standard ASGI server for FastAPI |
| LLM SDK | google-genai | Google's current official Gemini SDK |
| Configuration | python-dotenv | Keeps the API key in `.env`, out of source control |

## 8. How a Prompt Gets "Improved"

Every improved prompt follows the same repeatable recipe, which is itself the
lesson the application teaches:

1. **Role** — tell the model who it is (e.g. "You are an experienced editor").
2. **Context** — state what the input is and what it is for.
3. **Explicit constraints** — length, what to keep, what to avoid.
4. **Output format** — bullets, a JSON schema, "return only the rewrite", and so on.
5. **Edge-case handling** — "use null if missing", "use 'unknown' if unclear", "don't guess".

That structure is what turns a vague request into output that is **useful** (it
answers the real need), **consistent** (the same shape every run), and
**structured** (parseable and ready to use).

## 9. Challenges and How They Were Handled

- **Model availability and naming.** Google rotates Gemini model names over time, and an initially chosen model was found to be retired for new API keys. This was handled by making the model name a single configuration value and by querying the API for the models actually available to the key, then settling on a current, responsive model (`gemini-3.6-flash`).
- **Transient capacity errors.** Newer flash models occasionally returned "high demand" (HTTP 503) responses. The Gemini client was given a bounded timeout and automatic retries, and the UI surfaces a clear "model is busy, try again" message rather than hanging.
- **Keeping secrets safe.** Rather than calling Gemini from the browser, all API access was placed behind the back end so the key is never shipped to the client.
- **Consistent, fair comparison.** Both prompts are always run against the exact same input, so any difference in output is attributable to the prompt alone.

## 10. How to Run the Project

**Prerequisites:** Python 3.10+, Node.js 18+, and a Gemini API key (free from Google AI Studio).

On Windows, a one-time setup script installs all dependencies and a run script
starts both servers together:

- `setup.ps1` (or `setup.bat`) — creates the Python virtual environment, installs back-end and front-end dependencies, and creates the `.env` file.
- Add the API key to `backend/.env` as `GEMINI_API_KEY`.
- `run.ps1` (or `run.bat`) — launches the back end on port 8000 and the front end on port 5173, each in its own window, and opens the browser.

The application is then available at **http://localhost:5173**, and the
automatically generated API documentation at **http://localhost:8000/docs**.

## 11. Results

The application runs end to end against the live Gemini API. In testing, the
contrast is immediate and consistent across all five tasks: the improved prompts
return output in the requested format every time — three tight bullets for
summaries, valid JSON for classification and extraction, a single clean rewrite,
and on-brief marketing copy — whereas the lazy prompts vary in length, structure,
and tone from run to run. The side-by-side layout makes the value of prompt
engineering obvious within a single click.

## 12. Future Work

- A one-click "self-healing" model fallback that tries the latest flash model and drops back automatically when it is busy.
- A copy-to-clipboard button and the ability to save or share a comparison.
- A field for users to write and test their own prompt against the improved one.
- Automatic scoring of outputs (length, valid-JSON check) to quantify the improvement, not just show it.

## 13. Conclusion

Prompt Improvement Lab turns an abstract best practice — write structured prompts —
into something a user can see and feel. By pairing lazy and engineered prompts on
identical inputs and explaining the difference, it serves equally as a learning
tool, a developer sandbox, and a demonstration. The clean separation between data,
configuration, and the single Gemini-facing module also makes it a solid,
extensible foundation that can grow to more tasks or a different model with
minimal change.

---
