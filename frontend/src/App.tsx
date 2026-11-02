import { useEffect, useMemo, useState } from "react";
import { fetchTasks, runPrompt } from "./api";
import type { Task, Variant } from "./types";
import TaskSelector from "./components/TaskSelector";
import PromptCard from "./components/PromptCard";
import OutputPanel from "./components/OutputPanel";
import ExplanationCard from "./components/ExplanationCard";

interface PanelState {
  output: string | null;
  error: string | null;
  loading: boolean;
  latencyMs: number | null;
}

const EMPTY_PANEL: PanelState = {
  output: null,
  error: null,
  loading: false,
  latencyMs: null,
};

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [activeId, setActiveId] = useState<string>("");
  const [input, setInput] = useState<string>("");

  const [original, setOriginal] = useState<PanelState>(EMPTY_PANEL);
  const [improved, setImproved] = useState<PanelState>(EMPTY_PANEL);

  const activeTask = useMemo(
    () => tasks.find((t) => t.id === activeId),
    [tasks, activeId]
  );

  // Load the task definitions once on mount.
  useEffect(() => {
    fetchTasks()
      .then((data) => {
        setTasks(data);
        if (data.length > 0) {
          setActiveId(data[0].id);
          setInput(data[0].sample_input);
        }
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  function selectTask(id: string) {
    const task = tasks.find((t) => t.id === id);
    if (!task) return;
    setActiveId(id);
    setInput(task.sample_input);
    setOriginal(EMPTY_PANEL);
    setImproved(EMPTY_PANEL);
  }

  async function runVariant(
    variant: Variant,
    setPanel: (s: PanelState) => void
  ) {
    if (!activeTask) return;
    setPanel({ ...EMPTY_PANEL, loading: true });
    try {
      const res = await runPrompt(activeTask.id, variant, input);
      setPanel({
        output: res.output,
        error: null,
        loading: false,
        latencyMs: res.latency_ms,
      });
    } catch (err) {
      setPanel({
        output: null,
        error: err instanceof Error ? err.message : "Something went wrong.",
        loading: false,
        latencyMs: null,
      });
    }
  }

  function runComparison() {
    // Fire both at once so the two outputs come back together.
    runVariant("original", setOriginal);
    runVariant("improved", setImproved);
  }

  const busy = original.loading || improved.loading;
  const canRun = Boolean(activeTask) && input.trim().length > 0 && !busy;

  if (loadError) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
        <div className="max-w-md rounded-xl border border-red-200 bg-white p-6 text-center shadow-sm">
          <h1 className="mb-2 text-lg font-semibold text-slate-800">
            Can't reach the backend
          </h1>
          <p className="text-sm text-slate-600">{loadError}</p>
          <p className="mt-3 text-sm text-slate-500">
            Make sure the FastAPI server is running on port 8000
            (<code className="rounded bg-slate-100 px-1">uvicorn app:app --port 8000</code>).
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Prompt Improvement Lab
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Pick a task, run the lazy prompt and the improved one on the same
            input, and see the difference side by side.
          </p>
        </header>

        {/* Task tabs */}
        <TaskSelector tasks={tasks} activeId={activeId} onSelect={selectTask} />

        {activeTask && (
          <div className="mt-6 space-y-6">
            <p className="text-sm text-slate-600">{activeTask.description}</p>

            {/* Input + prompts */}
            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Input text
              </label>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={5}
                className="w-full resize-y rounded-lg border border-slate-200 p-3 text-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100"
                placeholder="Paste or edit the text to run…"
              />

              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <PromptCard
                  label="Original prompt"
                  variant="original"
                  prompt={activeTask.original_prompt}
                />
                <PromptCard
                  label="Improved prompt"
                  variant="improved"
                  prompt={activeTask.improved_prompt}
                />
              </div>

              <button
                onClick={runComparison}
                disabled={!canRun}
                className="mt-4 w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 sm:w-auto"
              >
                {busy ? "Running…" : "Run comparison"}
              </button>
            </div>

            {/* Outputs side by side */}
            <div className="flex flex-col gap-4 md:flex-row">
              <OutputPanel
                title="Original output"
                variant="original"
                output={original.output}
                error={original.error}
                loading={original.loading}
                latencyMs={original.latencyMs}
              />
              <OutputPanel
                title="Improved output"
                variant="improved"
                output={improved.output}
                error={improved.error}
                loading={improved.loading}
                latencyMs={improved.latencyMs}
              />
            </div>

            {/* Why it's better */}
            <ExplanationCard points={activeTask.explanation} />
          </div>
        )}
      </div>
    </div>
  );
}
