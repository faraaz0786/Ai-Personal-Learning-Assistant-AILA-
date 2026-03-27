import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, CheckCircle2, XCircle, AlertCircle } from "lucide-react";
import { twMerge } from "tailwind-merge";
import type { QuizAttemptResponse, QuizResponse } from "../../types/api";
import { TypewriterText } from "../atoms/TypewriterText";

type ResultsBreakdownProps = {
  quiz: QuizResponse;
  result: QuizAttemptResponse;
};

export function ResultsBreakdown({ quiz, result }: ResultsBreakdownProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const toggleAccordion = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="space-y-8 w-full max-w-5xl mx-auto">
      <div className="space-y-6">
        {quiz.questions.map((question, index) => {
          const item = result.results[index];
          const isOpen = openIndex === index;
          const isCorrect = item.correct;

          return (
            <div
              key={question.id}
              className={twMerge(
                "overflow-hidden rounded-[32px] border transition-all duration-300 bg-white",
                isOpen ? "border-primary-200 shadow-soft" : "border-surface-border shadow-sm hover:border-primary-100"
              )}
            >
              <button
                type="button"
                onClick={() => toggleAccordion(index)}
                className={twMerge(
                  "flex w-full items-center justify-between p-8 text-left transition-colors outline-none",
                  isOpen ? "bg-primary-50/30" : "hover:bg-slate-50/50"
                )}
              >
                <div className="flex items-center gap-6 pr-6">
                  <div className={twMerge(
                    "flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border-2 shadow-sm transition-transform duration-300",
                    isCorrect 
                      ? "border-green-100 bg-green-500 text-white" 
                      : "border-orange-100 bg-orange-500 text-white",
                    isOpen && "scale-110"
                  )}>
                    {isCorrect ? <CheckCircle2 size={20} /> : <XCircle size={20} />}
                  </div>
                  <span className="font-black text-slate-800 text-xl tracking-tight leading-tight">
                    {index + 1}. {question.question}
                  </span>
                </div>
                <motion.div
                  animate={{ rotate: isOpen ? 180 : 0 }}
                  transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                >
                  <ChevronDown className="h-6 w-6 text-slate-400" />
                </motion.div>
              </button>

              <AnimatePresence>
                {isOpen && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                  >
                    <div className="px-8 pb-10 pt-2 space-y-8 border-t border-surface-border/50">
                      <div className="grid gap-6 sm:grid-cols-2 mt-4">
                        <div className={twMerge(
                          "rounded-3xl p-6 border shadow-inner-soft",
                          isCorrect 
                            ? "bg-green-50/50 border-green-100" 
                            : "bg-orange-50/50 border-orange-100"
                        )}>
                          <p className={twMerge(
                            "text-[10px] font-black uppercase tracking-[0.2em] mb-3",
                            isCorrect ? "text-green-600" : "text-orange-600"
                          )}>Selected Path</p>
                          <p className={twMerge(
                            "text-lg font-black tracking-tight",
                            isCorrect ? "text-green-800" : "text-orange-900"
                          )}>
                            {question.options[item.your_answer] ?? <span className="text-slate-400 italic">No selection recorded</span>}
                          </p>
                        </div>
                        <div className="rounded-3xl bg-primary-50/50 p-6 border border-primary-100 shadow-inner-soft">
                          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-primary-600 mb-3">Target Mastery</p>
                          <p className="text-lg font-black text-primary-800 tracking-tight">
                            {question.options[item.correct_index]}
                          </p>
                        </div>
                      </div>

                      <div className="rounded-[32px] bg-slate-50 p-8 border border-surface-border relative overflow-hidden group">
                        <div className="absolute left-0 top-0 h-full w-2 bg-primary-600 group-hover:w-3 transition-all duration-300" />
                        <div className="flex items-center gap-3 text-primary-600 font-black mb-4 tracking-[0.1em] uppercase text-[10px]">
                          <AlertCircle className="h-4 w-4" />
                          <span>AI Intelligence Log</span>
                        </div>
                        <div className="leading-relaxed text-slate-700 font-medium text-lg italic">
                          <TypewriterText text={`"${question.explanation}"`} delay={300} speed={20} />
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </div>
  );
}
