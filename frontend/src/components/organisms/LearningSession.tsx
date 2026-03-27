import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { Link, useNavigate } from "react-router-dom";
import { 
  History, 
  Sparkles, 
  BookOpen, 
  Target,
  ChevronRight,
  Brain
} from "lucide-react";

import { explainTopic, generateQuiz } from "../../api/learning";
import { useQuizStore } from "../../store/quizStore";
import { useLearnStore } from "../../store/learnStore";
import { useUserStore } from "../../store/userStore";
import { useHistoryStore } from "../../store/historyStore";
import type {
  ApiErrorResponse,
  ExplainRequest,
  ExplainResponse,
  QuizRequest,
  QuizResponse,
} from "../../types/api";
import { ErrorState } from "../feedback/ErrorState";
import { SkeletonCard } from "../feedback/SkeletonCard";
import { ExplanationCard } from "../learning/ExplanationCard";
import { SummaryCard } from "../learning/SummaryCard";
import { TopicComposer } from "../learning/TopicComposer";
import { Button } from "../atoms/Button";

export function LearningSession() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const setQuiz = useQuizStore((state) => state.setQuiz);

  // --- Persistent state ---
  const topic = useLearnStore((s) => s.topic);
  const subject = useLearnStore((s) => s.subject);
  const storedResponse = useLearnStore((s) => s.response);
  const setTopic = useLearnStore((s) => s.setTopic);
  const setSubject = useLearnStore((s) => s.setSubject);
  const setStoredResponse = useLearnStore((s) => s.setResponse);

  const [validationMessage, setValidationMessage] = useState("");

  const addHistoryItem = useHistoryStore((s: any) => s.addHistoryItem);
  const historyItems = useHistoryStore((s: any) => s.items);
  const addPoints = useUserStore((s: any) => s.addPoints);
  const incrementEnquiries = useUserStore((s: any) => s.incrementEnquiries);

  const explainMutation = useMutation<
    ExplainResponse,
    AxiosError<ApiErrorResponse>,
    ExplainRequest
  >({
    mutationFn: explainTopic,
    onSuccess: (data) => {
      setStoredResponse(data);
      addHistoryItem(data.normalized_topic);
      incrementEnquiries();
      addPoints(10); // Reward for enquiry

      // Invalidate to refresh sidebar
      queryClient.invalidateQueries({ queryKey: ["progress-summary"] });
      queryClient.invalidateQueries({ queryKey: ["mentor-tip"] });
      queryClient.invalidateQueries({ queryKey: ["scholar-library"] });
    },
  });

  const quizMutation = useMutation<QuizResponse, AxiosError<ApiErrorResponse>, QuizRequest>({
    mutationFn: generateQuiz,
    onSuccess: (quiz) => {
      setQuiz(quiz);
      addPoints(50); // Mastery reward
      
      // Invalidate
      queryClient.invalidateQueries({ queryKey: ["progress-summary"] });
      
      navigate("/quiz");
    }
  });

  const response = explainMutation.data ?? storedResponse;
  let explainError =
    explainMutation.error?.response?.data?.error?.message ?? explainMutation.error?.message ?? null;

  if (explainMutation.isSuccess && (!explainMutation.data || !explainMutation.data.explanation)) {
    explainError = "Invalid response format from AI. Please retry.";
  }

  const handleSubmit = async (overrideTopic?: string) => {
    const activeTopic = (overrideTopic ?? topic).trim();
    if (activeTopic.length < 3) {
      setValidationMessage("Please enter at least 3 characters.");
      return;
    }
    setTopic(activeTopic);
    setValidationMessage("");
    await explainMutation.mutateAsync({ topic: activeTopic, subject });
  };

  const handleGenerateQuiz = async () => {
    if (!response?.topic_id) return;
    await quizMutation.mutateAsync({
      topic_id: response.topic_id,
      count: 5,
      difficulty: "medium"
    });
  };

  const handleHistoryClick = (h: string) => {
    setTopic(h);
    handleSubmit(h);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] bg-white rounded-3xl border border-surface-border shadow-academic overflow-hidden relative">
      <div className="flex-1 flex overflow-hidden">
        {/* Sub-Sidebar: History/Stats */}
        <aside className="hidden md:flex flex-col w-72 border-r border-surface-border bg-background-alt/30 p-8 space-y-10 overflow-y-auto">
          <section>
            <h3 className="text-[10px] font-bold text-primary-500 uppercase tracking-widest mb-6 flex items-center gap-2">
              <History size={12} />
              Recent Enquiries
            </h3>
            <div className="space-y-4">
              {historyItems.length > 0 ? (
                historyItems.map((h: any) => (
                  <button 
                    key={h.id} 
                    onClick={() => handleHistoryClick(h.topic)}
                    className="w-full text-left group"
                  >
                    <span className="text-sm font-medium text-surface-text-secondary group-hover:text-primary-600 transition-colors block truncate">
                      {h.topic}
                    </span>
                    <span className="text-[10px] text-secondary-muted italic">
                      {new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </button>
                ))
              ) : (
                <p className="text-[10px] text-secondary-muted italic">No recent enquiries</p>
              )}
            </div>
          </section>

          <section>
            <h3 className="text-[10px] font-bold text-primary-500 uppercase tracking-widest mb-6 flex items-center gap-2">
              <Target size={12} />
              Maestorship
            </h3>
            <div className="p-4 rounded-2xl bg-white border border-surface-border shadow-sm">
              <p className="text-xs font-editorial italic text-surface-text-primary mb-3 leading-relaxed">
                {response 
                  ? `You are one step away from mastering '${response.normalized_topic}'.`
                  : "Begin an enquiry to track your path to mastery."
                }
              </p>
          <Link to="/quiz" className="block w-full">
            <Button 
              variant="outline" 
              className="w-full rounded-xl py-3 text-sm font-bold border-surface-border text-primary-600 hover:border-primary-300 group"
            >
              Take Mastery Quiz
              <ChevronRight size={14} className="ml-2 group-hover:translate-x-0.5 transition-transform" />
            </Button>
          </Link>
            </div>
          </section>
        </aside>

        {/* Main Content Space */}
        <main className="flex-1 flex flex-col bg-white overflow-y-auto hide-scrollbar scroll-smooth">
          <div className="flex-1 p-8 lg:p-12">
            <AnimatePresence mode="wait">
              {!response && !explainMutation.isPending && !explainError ? (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto space-y-8"
                >
                  <div className="w-20 h-20 rounded-3xl bg-primary-50 flex items-center justify-center text-primary-600 border border-primary-100 shadow-academic">
                    <Brain size={40} strokeWidth={1.5} />
                  </div>
                  <div className="space-y-3">
                    <h1 className="text-4xl font-editorial font-bold text-surface-text-primary tracking-tight">
                      What shall we <span className="text-primary-500 italic">unravel</span> today?
                    </h1>
                    <p className="text-secondary-muted font-medium text-sm leading-relaxed">
                      Enter a topic below to begin your scholarly exploration with AILA, your learning concierge.
                    </p>
                  </div>
                  <div className="flex flex-wrap justify-center gap-2">
                    {['String Theory', 'Industrial Revolution', 'Cognitive Dissonance'].map(t => (
                      <button 
                        key={t}
                        onClick={() => handleSubmit(t)}
                        className="px-4 py-2 rounded-full border border-surface-border bg-background-alt/50 text-xs font-bold text-secondary-muted hover:text-primary-600 hover:border-primary-300 transition-all"
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </motion.div>
              ) : (
                <div className="max-w-3xl mx-auto space-y-12">
                  {explainError ? (
                    <ErrorState message={explainError} onRetry={() => handleSubmit()} />
                  ) : explainMutation.isPending ? (
                    <div className="space-y-8">
                      <div className="flex items-center gap-4 mb-4">
                        <Sparkles className="text-primary-400 animate-pulse" size={20} />
                        <span className="text-sm font-bold text-secondary-muted tracking-widest uppercase">Consulting the Knowledge Repository...</span>
                      </div>
                      <SkeletonCard lines={10} />
                      <SkeletonCard lines={6} />
                    </div>
                  ) : (
                    <motion.div 
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="space-y-12"
                    >
                      {response && (
                        <>
                          <ExplanationCard response={response} />
                          <SummaryCard response={response} />
                        </>
                      )}
                    </motion.div>
                  )}
                </div>
              )}
            </AnimatePresence>
          </div>
        </main>
      </div>

      {/* Bottom Fixed AI Input Bar */}
      <div className="border-t border-surface-border bg-white p-2">
        <TopicComposer
          topic={topic}
          subject={subject}
          validationMessage={validationMessage}
          loading={explainMutation.isPending}
          onTopicChange={setTopic}
          onSubjectChange={(v) => setSubject(v ?? "General")}
          onSubmit={() => handleSubmit()}
        />
      </div>
    </div>
  );
}
