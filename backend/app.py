"""FastAPI backend for the Prompt Improvement Lab.

Two routes: one to hand the frontend the task definitions, one to run a single
prompt (original or improved) through Gemini.
"""

import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config
import gemini_client
from prompts import TASKS, TASKS_BY_ID

app = FastAPI(title="Prompt Improvement Lab")

# Allow the Vite dev server (and common localhost variants) to call us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    task_id: str
    variant: str  # "original" or "improved"
    input: str


class RunResponse(BaseModel):
    output: str
    model: str
    latency_ms: int


@app.get("/api/tasks")
def list_tasks():
    """Return every task, including both prompt texts and the explanation."""
    return TASKS


@app.post("/api/run", response_model=RunResponse)
def run_prompt(req: RunRequest):
    task = TASKS_BY_ID.get(req.task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Unknown task: {req.task_id}")

    if req.variant == "original":
        template = task["original_prompt"]
    elif req.variant == "improved":
        template = task["improved_prompt"]
    else:
        raise HTTPException(
            status_code=400,
            detail="variant must be 'original' or 'improved'",
        )

    prompt = template.format(input=req.input)

    start = time.perf_counter()
    try:
        output = gemini_client.generate(prompt)
    except gemini_client.GeminiError as exc:
        # 400 when it's a config problem (missing key), 502 for upstream failures.
        status = 400 if "GEMINI_API_KEY" in str(exc) else 502
        raise HTTPException(status_code=status, detail=str(exc))
    latency_ms = int((time.perf_counter() - start) * 1000)

    return RunResponse(
        output=output,
        model=gemini_client.get_model_name(),
        latency_ms=latency_ms,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.HOST, port=config.PORT)
