import React from "react";
import { motion } from "framer-motion";
import { useUserStore } from "../../store/userStore";

export const ProgressTracker: React.FC = () => {
  const { progress } = useUserStore();

  return (
    <div className="scholarly-card p-6 border-l-4 border-l-primary-500">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-serif text-[#3e3a36]">Scholarly Progress</h3>
        <span className="text-2xl font-bold text-primary-500">{progress}%</span>
      </div>
      
      <div className="relative w-full h-3 bg-[#e8e2d8] rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="absolute top-0 left-0 h-full bg-primary-500 shadow-[0_0_10px_rgba(161,75,43,0.3)]"
        />
      </div>
      
      <p className="mt-4 text-sm text-[#6b645d] italic font-serif">
        {progress < 30 ? "Beginning your academic journey..." : 
         progress < 70 ? "Your understanding is deepening across multiple domains." : 
         "You are approaching mastery in your current studies."}
      </p>
    </div>
  );
};
