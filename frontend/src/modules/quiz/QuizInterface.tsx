import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, XCircle, ChevronRight, ChevronLeft, Lightbulb } from "lucide-react";
import { twMerge } from "tailwind-merge";

import { submitQuizAttempt } from "../../api/quiz";
import { useQuizStore } from "../../store/quizStore";
import type {
  ApiErrorResponse,
  QuizAttemptRequest,
  QuizAttemptResponse,
} from "../../types/api";
import { Button } from "../../components/atoms/Button";
import { EmptyState } from "../../components/feedback/EmptyState";
import { ErrorState } from "../../components/feedback/ErrorState";

export function QuizInterface() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const {
    currentQuiz,
    answers,
    revealedQuestionIds,
    currentQuestionIndex,
    selectAnswer,
    revealQuestion,
    nextQuestion,
    previousQuestion,
    setAttemptResult
  } = useQuizStore();

  const submitAttemptMutation = useMutation<
    QuizAttemptResponse,
    AxiosError<ApiErrorResponse>,
    QuizAttemptRequest
  >({
    mutationFn: async (payload) => {
      if (!currentQuiz) {
        throw new Error("Quiz not available.");
      }
      return submitQuizAttempt(currentQuiz.quiz_id, payload);
    },
    onSuccess: (result) => {
      setAttemptResult(result);
      
      // Invalidate to refresh sidebar and library
      queryClient.invalidateQueries({ queryKey: ["progress-summary"] });
      queryClient.invalidateQueries({ queryKey: ["mentor-tip"] });
      queryClient.invalidateQueries({ queryKey: ["scholar-library"] });
      
      navigate("/quiz/results");
    }
  });

  if (!currentQuiz) {
    return (
      <EmptyState
        title="No active quiz found"
        description="Generate a quiz from the learning session to start practicing."
        actionLabel="Back to Learning"
        actionTo="/learn"
      />
    );
  }

  const question = currentQuiz.questions[currentQuestionIndex];
  const selectedAnswer = answers[question.id];
  const isRevealed = revealedQuestionIds.includes(question.id);
  const allQuestionsRevealed =
    currentQuiz.questions.length === revealedQuestionIds.length;
  const submitError =
    submitAttemptMutation.error?.response?.data?.error?.message ??
    submitAttemptMutation.error?.message;

  const handleReveal = () => {
    if (selectedAnswer === undefined) {
      return;
    }
    revealQuestion(question.id);
  };

  const handleFinishQuiz = async () => {
    await submitAttemptMutation.mutateAsync({
      answers: currentQuiz.questions.map((item) => answers[item.id] ?? 0)
    });
  };

  const progressPercentage = ((currentQuestionIndex + 1) / currentQuiz.questions.length) * 100;

  return (
    <div className="bg-white border border-surface-border shadow-soft rounded-[48px] flex flex-col p-10 sm:p-16 transition-all duration-500 max-w-5xl mx-auto w-full relative overflow-hidden">
      {/* Subtle background accent */}
      <div className="absolute top-0 left-0 w-full h-1.5 bg-primary-600" />
      
      {/* Header & Progress */}
      <div className="mb-14 space-y-6">
        <div className="flex items-center justify-between text-[11px] font-black tracking-[0.3em] uppercase text-slate-400">
          <span className="flex items-center gap-3">
            <span className="w-8 h-8 rounded-xl bg-primary-50 text-primary-600 flex items-center justify-center border border-primary-100 shadow-sm">
              {currentQuestionIndex + 1}
            </span>
            Step {currentQuestionIndex + 1} / {currentQuiz.questions.length}
          </span>
          <span className="text-primary-600">Verification {Math.round(progressPercentage)}%</span>
        </div>
        <div className="h-4 w-full overflow-hidden rounded-2xl bg-slate-50 border border-surface-border p-1 shadow-inner-soft">
          <motion.div
            className="h-full bg-primary-600 rounded-xl shadow-soft"
            initial={{ width: 0 }}
            animate={{ width: `${progressPercentage}%` }}
            transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={question.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col gap-10"
        >
          {/* Question Title */}
          <h2 className="text-3xl font-black leading-tight text-slate-800 sm:text-4xl tracking-tight">
            {question.question}
          </h2>

          {/* Options */}
          <div className="grid gap-5" role="radiogroup" aria-label="Quiz options">
            {question.options.map((option, index) => {
              const isSelected = selectedAnswer === index;
              const isCorrect = isRevealed && index === question.correct_index;
              const isIncorrectSelection =
                isRevealed && isSelected && index !== question.correct_index;

              let stateClass = "border-surface-border bg-white text-slate-700 hover:border-primary-200 hover:bg-slate-50 shadow-sm";
              
              if (isCorrect) {
                stateClass = "border-green-500 bg-green-50 text-green-900 shadow-soft scale-[1.01]";
              } else if (isIncorrectSelection) {
                stateClass = "border-orange-500 bg-orange-50 text-orange-900 shadow-soft";
              } else if (isSelected) {
                stateClass = "border-primary-600 bg-primary-600 text-white shadow-xl shadow-primary-200/50 scale-[1.01]";
              }

              return (
                <motion.button
                  key={`${question.id}-${index}`}
                  type="button"
                  whileHover={!isRevealed ? { x: 8 } : {}}
                  whileTap={!isRevealed ? { scale: 0.99 } : {}}
                  onClick={() => !isRevealed && selectAnswer(question.id, index)}
                  role="radio"
                  aria-checked={isSelected}
                  disabled={isRevealed}
                  className={twMerge(
                    "group relative flex items-center justify-between overflow-hidden rounded-[24px] border p-6 text-left transition-all duration-300",
                    stateClass
                  )}
                >
                  <div className="flex items-center gap-6">
                    <span className={twMerge(
                      "flex h-10 w-10 items-center justify-center rounded-xl border-2 text-sm font-black transition-all duration-300 shadow-sm",
                      isSelected && !isRevealed ? "border-white/30 bg-white/20" : 
                      isCorrect ? "border-green-400 bg-green-500 text-white" :
                      isIncorrectSelection ? "border-orange-400 bg-orange-500 text-white" :
                      "border-slate-100 bg-slate-50 text-slate-400 group-hover:border-primary-100 group-hover:text-primary-600"
                    )}>
                      {String.fromCharCode(65 + index)}
                    </span>
                    <span className="text-xl font-black tracking-tight leading-relaxed">{option}</span>
                  </div>
                  
                  {isRevealed && isCorrect && (
                    <motion.div initial={{ scale: 0, rotate: -20 }} animate={{ scale: 1, rotate: 0 }}>
                      <CheckCircle2 className="h-8 w-8 text-green-600" />
                    </motion.div>
                  )}
                  {isRevealed && isIncorrectSelection && (
                    <motion.div initial={{ scale: 0, rotate: 20 }} animate={{ scale: 1, rotate: 0 }}>
                      <XCircle className="h-8 w-8 text-orange-600" />
                    </motion.div>
                  )}
                </motion.button>
              );
            })}
          </div>

          {/* Explanation */}
          <AnimatePresence>
            {isRevealed && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                className="mt-4"
              >
                <div className="rounded-[32px] bg-slate-50 p-8 border border-surface-border relative overflow-hidden group">
                  <div className="absolute left-0 top-0 h-full w-2 bg-primary-600" />
                  <div className="flex items-center gap-3 text-primary-600 font-black mb-4 tracking-[0.1em] uppercase text-[10px]">
                    <Lightbulb size={18} />
                    Educational Intelligence
                  </div>
                  <p className="text-slate-700 leading-relaxed text-lg font-medium italic">
                    "{question.explanation}"
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Controls */}
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-between gap-6 pt-10 border-t border-surface-border">
            <Button
              variant="outline"
              size="lg"
              className="w-full sm:w-auto px-10 h-16 rounded-2xl"
              onClick={previousQuestion}
              disabled={currentQuestionIndex === 0}
            >
              <ChevronLeft className="mr-3 h-5 w-5" /> Previous Core
            </Button>

            {!isRevealed ? (
              <Button 
                size="lg"
                className="w-full sm:w-auto px-14 h-16 rounded-2xl"
                onClick={handleReveal} 
                disabled={selectedAnswer === undefined}
              >
                Execute Verification
              </Button>
            ) : currentQuestionIndex < currentQuiz.questions.length - 1 ? (
              <Button 
                size="lg"
                className="w-full sm:w-auto px-14 h-16 rounded-2xl animate-pulse-soft"
                onClick={nextQuestion}
              >
                Next Challenge <ChevronRight className="ml-3 h-5 w-5" />
              </Button>
            ) : (
              <Button
                size="lg"
                onClick={handleFinishQuiz}
                disabled={!allQuestionsRevealed || submitAttemptMutation.isPending}
                className="w-full sm:w-auto px-16 h-16 rounded-2xl shadow-xl shadow-primary-200"
              >
                {submitAttemptMutation.isPending ? "Analyzing Path..." : "Complete Integration"}
              </Button>
            )}
          </div>

          {submitError && (
            <div className="mt-6">
              <ErrorState message={submitError} />
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
