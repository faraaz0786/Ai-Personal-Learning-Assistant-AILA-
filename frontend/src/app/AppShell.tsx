import { ReactNode } from "react";
import { Sidebar } from "../components/organisms/Sidebar";
import { ProgressTracker } from "../components/progress/ProgressTracker";
import { MentorTips } from "../components/insights/MentorTips";
import { useQuery } from "@tanstack/react-query";
import { getProgressSummary } from "../api/progress";
import { getMentorTip } from "../api/insights";
import { useUserStore } from "../store/userStore";
import { useEffect } from "react";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  const { updateProgress, setInsight } = useUserStore();

  // Sync Progress
  const { data: progressData } = useQuery({
    queryKey: ["progress-summary"],
    queryFn: () => getProgressSummary(),
    refetchInterval: 60000, // Refresh every minute
  });

  // Sync Mentor Tip
  const { data: tipData } = useQuery({
    queryKey: ["mentor-tip"],
    queryFn: () => getMentorTip(),
    refetchInterval: 120000, // Refresh every 2 minutes
  });

  useEffect(() => {
    if (progressData) {
      updateProgress(progressData.progress_percent);
    }
  }, [progressData, updateProgress]);

  useEffect(() => {
    if (tipData) {
      setInsight(tipData);
    }
  }, [tipData, setInsight]);

  return (
    <div className="flex min-h-screen bg-background text-surface-text-primary overflow-hidden">
      {/* Warm Ambient Background overlay */}
      <div className="fixed inset-0 bg-ivory-mesh pointer-events-none z-0" />
      
      {/* Left Sidebar - Fixed */}
      <Sidebar />

      {/* Main Area */}
      <main className="flex-1 flex flex-col min-w-0 h-screen relative z-10">
        <div className="flex-1 flex overflow-hidden">
          {/* Main Content Area - fluid but max-w-6xl */}
          <div className="flex-1 overflow-y-auto hide-scrollbar px-6 lg:px-12 py-12 scroll-smooth">
            <div className="max-w-4xl xl:max-w-5xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-1000">
              {children}
            </div>
          </div>

          {/* Right Panel - Dynamic Intelligence Panel */}
          <aside className="hidden xl:flex flex-col w-80 shrink-0 border-l border-surface-border bg-white/30 backdrop-blur-sm p-8 overflow-y-auto">
            <div className="space-y-8">
              <section>
                <ProgressTracker />
              </section>

              <section>
                <MentorTips />
              </section>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
}
