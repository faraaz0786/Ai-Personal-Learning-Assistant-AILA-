import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Lightbulb, Target, ArrowRight } from "lucide-react";
import { useUserStore } from "../../store/userStore";

export const MentorTips: React.FC = () => {
  const { currentInsight } = useUserStore();

  if (!currentInsight) {
    return (
      <div className="scholarly-card p-6 bg-[#fdfaf6] border border-[#e8e2d8] opacity-50">
        <p className="text-[#6b645d] italic font-serif">
          Consulting the AI Mentor for insights...
        </p>
      </div>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={currentInsight.tip}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className="scholarly-card p-6 bg-[#fdfaf6] border-l-4 border-l-primary-500 shadow-sm"
      >
        <div className="flex items-start gap-4">
          <div className="p-2 bg-[#f5f1eb] rounded-lg border border-[#e8e2d8]">
            <Lightbulb className="w-5 h-5 text-primary-500" />
          </div>
          <div className="flex-1">
            <h4 className="text-sm font-bold uppercase tracking-wider text-primary-500 mb-1">
              AI Mentor Insight
            </h4>
            <p className="text-[#3e3a36] font-medium leading-relaxed mb-3">
              "{currentInsight.tip}"
            </p>
            
            <div className="flex items-center gap-2 text-xs text-[#a14b2b] font-bold mt-4 pt-4 border-t border-[#e8e2d8]">
              <Target className="w-3.5 h-3.5" />
              <span>Focus Area: {currentInsight.focus_area}</span>
            </div>
            
            <div className="mt-3 flex items-center justify-between group cursor-pointer">
              <span className="text-xs text-[#6b645d]">{currentInsight.recommendation}</span>
              <ArrowRight className="w-4 h-4 text-primary-500 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};
