interface Props {
  points: string[];
}

export default function ExplanationCard({ points }: Props) {
  return (
    <div className="rounded-xl border border-indigo-100 bg-indigo-50/60 p-5">
      <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-indigo-800">
        <span aria-hidden>💡</span> Why the improved prompt is better
      </h3>
      <ul className="space-y-2">
        {points.map((point, i) => (
          <li key={i} className="flex gap-2 text-sm text-slate-700">
            <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-indigo-400" />
            <span>{point}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
