import type { ProgressHistoryItem } from "../../types/api";
import { Card } from "../molecules/Card";
import { Calendar, Ribbon } from "lucide-react";

type TopicsTableProps = {
  history: ProgressHistoryItem[];
};

export function TopicsTable({ history }: TopicsTableProps) {
  return (
    <Card 
      title="Recent Activity"
      className="border-slate-700/50 bg-slate-800/40 backdrop-blur-md shadow-xl"
    >
      <div className="overflow-x-auto pt-2">
        <table className="w-full text-left text-sm border-separate border-spacing-0">
          <thead>
            <tr>
              <th className="border-b border-slate-700/50 pb-3 pl-4 font-semibold text-slate-400">Topic</th>
              <th className="border-b border-slate-700/50 pb-3 font-semibold text-slate-400">Date</th>
              <th className="border-b border-slate-700/50 pb-3 pr-4 text-right font-semibold text-slate-400">Score</th>
            </tr>
          </thead>
          <tbody className="text-slate-200">
            {history.map((item, i) => (
              <tr 
                key={`${item.topic}-${item.attempted_at}`} 
                className={`group transition-colors hover:bg-slate-700/30 ${i !== history.length - 1 ? 'border-b border-slate-700/30' : ''}`}
              >
                <td className={`py-4 pl-4 font-medium text-white ${i !== history.length - 1 ? 'border-b border-slate-700/30' : ''}`}>
                  {item.topic}
                </td>
                <td className={`py-4 ${i !== history.length - 1 ? 'border-b border-slate-700/30' : ''}`}>
                  <div className="flex items-center gap-2 text-slate-400">
                    <Calendar className="h-4 w-4" />
                    {new Date(item.attempted_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                  </div>
                </td>
                <td className={`py-4 pr-4 text-right ${i !== history.length - 1 ? 'border-b border-slate-700/30' : ''}`}>
                  <div className="inline-flex items-center gap-1.5 rounded-full bg-slate-900/50 px-2.5 py-1 border border-slate-700/50 font-bold tracking-wide">
                    <Ribbon className={`h-3.5 w-3.5 ${item.score >= 80 ? 'text-emerald-400' : item.score >= 50 ? 'text-orange-400' : 'text-rose-400'}`} />
                    <span className={item.score >= 80 ? 'text-emerald-300' : item.score >= 50 ? 'text-orange-300' : 'text-rose-300'}>
                      {item.score}%
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
