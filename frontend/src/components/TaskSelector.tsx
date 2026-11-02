import type { Task } from "../types";

interface Props {
  tasks: Task[];
  activeId: string;
  onSelect: (id: string) => void;
}

export default function TaskSelector({ tasks, activeId, onSelect }: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      {tasks.map((task) => {
        const active = task.id === activeId;
        return (
          <button
            key={task.id}
            onClick={() => onSelect(task.id)}
            className={
              "rounded-full px-4 py-2 text-sm font-medium transition " +
              (active
                ? "bg-indigo-600 text-white shadow-sm"
                : "bg-white text-slate-600 ring-1 ring-slate-200 hover:bg-slate-50")
            }
          >
            {task.name}
          </button>
        );
      })}
    </div>
  );
}
