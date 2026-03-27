import { motion } from "framer-motion";
import { Link, Navigate } from "react-router-dom";
import { 
  Trophy, 
  ArrowRight, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle2, 
  Target,
  LineChart as LineChartIcon,
  BarChart3
} from "lucide-react";

import { useQuizStore } from "../store/quizStore";
import { Button } from "../components/atoms/Button";
import { StatsGrid } from "../components/dashboard/StatsGrid";
import { PerformanceChart } from "../components/dashboard/PerformanceChart";
import { AccuracyChart } from "../components/dashboard/AccuracyChart";
import { ResultsBreakdown } from "../components/quiz/ResultsBreakdown";
import { Card } from "../components/molecules/Card";

export function QuizResultsPage() {
  const { attemptResult, restartQuiz } = useQuizStore();

  if (!attemptResult) {
    return <Navigate to="/learn" replace />;
  }

  const { score, max_score, percentage, analytics, insights } = attemptResult;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div 
      className="pb-20 space-y-16"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* Header Section */}
      <motion.div variants={itemVariants} className="text-center space-y-6 pt-10">
        <div className="inline-flex items-center justify-center p-6 rounded-[32px] bg-primary-50 border border-primary-100 mb-2 shadow-soft">
          <Trophy className="h-14 w-14 text-primary-600" />
        </div>
        <h1 className="text-5xl md:text-6xl font-black text-slate-800 tracking-tight">Mastery Achieved.</h1>
        <p className="text-slate-500 max-w-2xl mx-auto text-lg font-medium leading-relaxed">
          Deep learning is a journey, not a destination. We've analyzed your performance 
          to identify the subtle patterns in your understanding.
        </p>
      </motion.div>

      {/* Main Score Card */}
      <motion.div variants={itemVariants} className="max-w-4xl mx-auto w-full">
        <div className="bg-white border border-surface-border rounded-[48px] shadow-soft p-12 sm:p-20 text-center relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1.5 bg-primary-600" />
          
          <div className="space-y-10">
            <div className="space-y-4">
              <span className="text-[10px] font-black uppercase tracking-[0.4em] text-primary-600 px-4 py-1.5 bg-primary-50 rounded-full inline-block">Workspace Score</span>
              <div className="flex items-center justify-center gap-6">
                <span className="text-9xl font-black text-slate-800 tracking-tighter leading-none">{score}</span>
                <span className="text-4xl font-black text-slate-200 mt-10">/ {max_score}</span>
              </div>
            </div>

            <div className="max-w-md mx-auto space-y-4">
              <div className="flex justify-between text-sm font-black text-slate-500 uppercase tracking-widest">
                <span>Accuracy Focus</span>
                <span className="text-primary-600">{percentage}%</span>
              </div>
              <div className="h-8 w-full rounded-2xl bg-slate-50 overflow-hidden border border-surface-border p-1.5 shadow-inner">
                <motion.div
                  className="h-full rounded-xl bg-primary-600 shadow-soft"
                  initial={{ width: 0 }}
                  animate={{ width: `${percentage}%` }}
                  transition={{ duration: 1.5, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-6 pt-10">
              <Button onClick={restartQuiz} variant="outline" size="lg" className="h-16 px-12 rounded-2xl">
                Retake Mastery
              </Button>
              <Link to="/learn">
                <Button size="lg" className="h-16 px-12 rounded-2xl animate-pulse-soft">
                  Continue Workspace <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Analytics Insights Grid */}
      {analytics && (
        <div className="space-y-16 max-w-7xl mx-auto w-full">
           <motion.div variants={itemVariants} className="flex items-center gap-4 border-b border-surface-border pb-8">
             <div className="h-12 w-3 rounded-full bg-primary-600" />
             <h2 className="text-4xl font-black text-slate-800 tracking-tight">Neural Analytics</h2>
           </motion.div>

           <motion.div variants={itemVariants}>
              <StatsGrid dashboard={analytics} />
           </motion.div>

           <div className="grid gap-10 lg:grid-cols-2">
              <Card title="Growth Trend" className="bg-white">
                <div className="flex items-center gap-3 text-slate-400 mb-8 px-2">
                  <LineChartIcon className="h-5 w-5 text-primary-500" />
                  <span className="text-[10px] font-black uppercase tracking-widest">Score Evolution Over Time</span>
                </div>
                <PerformanceChart data={analytics.performance_trend} />
              </Card>

              <Card title="Mastery Matrix" className="bg-white">
                <div className="flex items-center gap-3 text-slate-400 mb-8 px-2">
                  <BarChart3 className="h-5 w-5 text-primary-500" />
                  <span className="text-[10px] font-black uppercase tracking-widest">Accuracy Ranking by Topic</span>
                </div>
                <AccuracyChart data={analytics.top_topics} />
              </Card>
           </div>

           {/* AI Deep Insights */}
           {insights && (
             <motion.div variants={itemVariants} className="space-y-10">
                <div className="flex items-center gap-4 border-b border-surface-border pb-8">
                  <div className="h-12 w-3 rounded-full bg-primary-100" />
                  <h2 className="text-4xl font-black text-slate-800 tracking-tight">AI Diagnostic</h2>
                </div>

                <div className="grid gap-8 md:grid-cols-2">
                  <div className="bg-white border border-surface-border rounded-[40px] p-10 space-y-6 shadow-sm group hover:border-green-200 transition-colors duration-300">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-green-50 border border-green-100 flex items-center justify-center text-green-600">
                        <CheckCircle2 size={24} />
                      </div>
                      <h3 className="font-black uppercase tracking-widest text-[10px] text-green-600">Cognitive Strengths</h3>
                    </div>
                    <p className="text-slate-600 font-medium leading-relaxed text-lg">{insights.strengths}</p>
                  </div>

                  <div className="bg-white border border-surface-border rounded-[40px] p-10 space-y-6 shadow-sm group hover:border-orange-200 transition-colors duration-300">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-orange-50 border border-orange-100 flex items-center justify-center text-orange-600">
                        <AlertCircle size={24} />
                      </div>
                      <h3 className="font-black uppercase tracking-widest text-[10px] text-orange-600">Learning Gaps</h3>
                    </div>
                    <p className="text-slate-600 font-medium leading-relaxed text-lg">{insights.weaknesses}</p>
                  </div>

                  <div className="bg-white border border-surface-border rounded-[40px] p-10 space-y-6 shadow-sm group hover:border-primary-200 transition-colors duration-300">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-primary-50 border border-primary-100 flex items-center justify-center text-primary-600">
                        <TrendingUp size={24} />
                      </div>
                      <h3 className="font-black uppercase tracking-widest text-[10px] text-primary-600">Neural Optimization</h3>
                    </div>
                    <p className="text-slate-600 font-medium leading-relaxed text-lg">{insights.what_to_improve}</p>
                  </div>

                  <div className="bg-primary-600 rounded-[40px] p-10 space-y-6 shadow-xl shadow-primary-200">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-white">
                        <Target size={24} />
                      </div>
                      <h3 className="font-black uppercase tracking-widest text-[10px] text-white/70">Assistant Recommendation</h3>
                    </div>
                    <p className="text-white font-medium leading-relaxed text-lg">{insights.recommendation}</p>
                  </div>
                </div>
             </motion.div>
           )}

           {/* Detailed Question Review */}
           <motion.div variants={itemVariants} className="space-y-10 pt-10">
              <div className="flex items-center gap-4 border-b border-surface-border pb-8">
                <div className="h-12 w-3 rounded-full bg-slate-800" />
                <h2 className="text-4xl font-black text-slate-800 tracking-tight">Review Session</h2>
              </div>
              <ResultsBreakdown quiz={useQuizStore.getState().currentQuiz!} result={attemptResult} />
           </motion.div>
        </div>
      )}
    </motion.div>
  );
}
