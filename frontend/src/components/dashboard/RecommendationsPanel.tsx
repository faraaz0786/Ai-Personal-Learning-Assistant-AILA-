import { Lightbulb, Wrench, RefreshCw, Zap } from "lucide-react";
import type { ProgressRecommendation } from "../../types/api";
import { Card } from "../molecules/Card";

type RecommendationsPanelProps = {
  recommendations: ProgressRecommendation[];
};

export function RecommendationsPanel({ recommendations }: RecommendationsPanelProps) {
  return (
    <Card 
      title="Actionable Insights" 
      className="border-slate-700/50 bg-slate-800/40 backdrop-blur-md shadow-xl"
    >
      <div className="space-y-4 pt-2">
        {recommendations.map((item) => {
          let Icon = Lightbulb;
          let colorClass = "text-blue-400";
          let bgClass = "bg-blue-500/10 border-blue-500/20";
          
          if (item.type.toLowerCase() === 'review') {
            Icon = RefreshCw;
            colorClass = "text-orange-400";
            bgClass = "bg-orange-500/10 border-orange-500/20";
          } else if (item.type.toLowerCase() === 'practice') {
            Icon = Wrench;
            colorClass = "text-emerald-400";
            bgClass = "bg-emerald-500/10 border-emerald-500/20";
          } else if (item.type.toLowerCase() === 'challenge') {
            Icon = Zap;
            colorClass = "text-purple-400";
            bgClass = "bg-purple-500/10 border-purple-500/20";
          }

          return (
            <div 
              key={`${item.topic}-${item.type}`} 
              className={`group flex gap-4 rounded-2xl border p-4 transition-all duration-300 hover:bg-slate-700/30 ${bgClass}`}
            >
              <div className={`mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-800/50 border border-slate-700/50 shadow-inner group-hover:scale-110 transition-transform`}>
                <Icon className={`h-5 w-5 ${colorClass}`} />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <p className="font-semibold text-white drop-shadow-sm">{item.topic}</p>
                  <span className={`rounded-full px-2.5 py-0.5 text-[0.65rem] font-bold uppercase tracking-wider ${colorClass} bg-slate-900/50 border border-slate-700/50`}>
                    {item.type}
                  </span>
                </div>
                <p className="mt-1.5 leading-relaxed text-sm text-slate-300">{item.reason}</p>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
