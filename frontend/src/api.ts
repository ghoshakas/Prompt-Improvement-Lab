import type { RunResponse, Task, Variant } from "./types";

const API_BASE =
  (import.meta.env.VITE_API_BASE as string | undefined) ??
  "http://localhost:8000";

export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch(`${API_BASE}/api/tasks`);
  if (!res.ok) {
    throw new Error(`Couldn't load tasks (HTTP ${res.status}).`);
  }
  return res.json();
}

export async function runPrompt(
  taskId: string,
  variant: Variant,
  input: string
): Promise<RunResponse> {
  const res = await fetch(`${API_BASE}/api/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task_id: taskId, variant, input }),
  });

  if (!res.ok) {
    let detail = `Request failed (HTTP ${res.status}).`;
    try {
      const body = await res.json();
      if (body?.detail) detail = body.detail;
    } catch {
      /* non-JSON error body — keep the generic message */
    }
    throw new Error(detail);
  }

  return res.json();
}
