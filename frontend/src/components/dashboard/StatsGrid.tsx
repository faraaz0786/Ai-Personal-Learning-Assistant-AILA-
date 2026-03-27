import { BookOpen, BrainCircuit, Target, Flame } from "lucide-react";
import type { DashboardSummary } from "../../types/api";
import { twMerge } from "tailwind-merge";

type StatsGridProps = {
  dashboard: DashboardSummary;
};

export function StatsGrid({ dashboard }: StatsGridProps) {
  const stats = [
    {
      title: "Topics Studied",
      value: dashboard.total_topics,
      icon: BookOpen,
      color: "text-primary-600",
      bg: "bg-primary-50",
      border: "border-primary-100"
    },
    {
      title: "Questions Answered",
      value: dashboard.total_questions,
      icon: BrainCircuit,
      color: "text-primary-600",
      bg: "bg-primary-50",
      border: "border-primary-100"
    },
    {
      title: "Average Accuracy",
      value: `${dashboard.accuracy}%`,
      icon: Target,
      color: "text-green-600",
      bg: "bg-green-50",
      border: "border-green-100"
    },
    {
      title: "Current Streak",
      value: `${dashboard.streak} Days`,
      icon: Flame,
      color: "text-orange-600",
      bg: "bg-orange-50",
      border: "border-orange-100"
    }
  ];

  return (
    <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => {
        const Icon = stat.icon;
        
        return (
          <div
            key={stat.title}
            className="group relative overflow-hidden rounded-[32px] border border-surface-border bg-white p-8 shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1"
          >
            <div className="relative z-10 flex flex-col gap-6">
              <div className={twMerge(
                "flex h-14 w-14 items-center justify-center rounded-2xl border transition-all duration-300 group-hover:scale-110 shadow-sm",
                stat.bg, stat.border, stat.color
              )}>
                <Icon className="h-7 w-7" />
              </div>
              <div>
                <p className="text-[10px] font-black tracking-[0.2em] text-slate-400 uppercase">{stat.title}</p>
                <p className="mt-1 text-4xl font-black text-slate-800 tracking-tight">
                  {stat.value}
                </p>
              </div>
            </div>
            {/* Soft decorative glow */}
            <div className={twMerge(
              "absolute -bottom-10 -right-10 h-32 w-32 rounded-full opacity-10 blur-3xl group-hover:opacity-20 transition-opacity duration-700",
              stat.bg
            )} />
          </div>
        );
      })}
    </div>
  );
}
