import { useState } from "react";

interface Props {
  label: string;
  variant: "original" | "improved";
  prompt: string;
}

export default function PromptCard({ label, variant, prompt }: Props) {
  const [open, setOpen] = useState(false);
  const improved = variant === "improved";

  return (
    <div
      className={
        "rounded-lg border p-3 text-sm " +
        (improved
          ? "border-emerald-200 bg-emerald-50/50"
          : "border-slate-200 bg-slate-50")
      }
    >
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between text-left"
      >
        <span
          className={
            "font-semibold " +
            (improved ? "text-emerald-700" : "text-slate-600")
          }
        >
          {label}
        </span>
        <span className="text-xs text-slate-400">
          {open ? "Hide prompt ▲" : "Show prompt ▼"}
        </span>
      </button>
      {open && (
        <pre className="mt-2 whitespace-pre-wrap break-words font-mono text-xs leading-relaxed text-slate-700">
          {prompt}
        </pre>
      )}
    </div>
  );
}
