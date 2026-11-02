interface Props {
  title: string;
  variant: "original" | "improved";
  output: string | null;
  error: string | null;
  loading: boolean;
  latencyMs: number | null;
}

export default function OutputPanel({
  title,
  variant,
  output,
  error,
  loading,
  latencyMs,
}: Props) {
  const improved = variant === "improved";

  return (
    <div className="flex flex-1 flex-col rounded-xl border border-slate-200 bg-white shadow-sm">
      <div
        className={
          "flex items-center justify-between rounded-t-xl px-4 py-2.5 " +
          (improved ? "bg-emerald-600" : "bg-slate-500")
        }
      >
        <h3 className="text-sm font-semibold text-white">{title}</h3>
        {latencyMs != null && !loading && (
          <span className="text-xs text-white/80">{latencyMs} ms</span>
        )}
      </div>

      <div className="min-h-[9rem] flex-1 p-4 text-sm">
        {loading ? (
          <div className="flex h-full items-center gap-2 text-slate-400">
            <span className="h-3 w-3 animate-spin rounded-full border-2 border-slate-300 border-t-slate-500" />
            Running…
          </div>
        ) : error ? (
          <p className="rounded-md bg-red-50 p-3 text-red-700">{error}</p>
        ) : output ? (
          <pre className="whitespace-pre-wrap break-words font-mono text-[13px] leading-relaxed text-slate-800">
            {output}
          </pre>
        ) : (
          <p className="text-slate-400">
            Run a comparison to see the output here.
          </p>
        )}
      </div>
    </div>
  );
}
