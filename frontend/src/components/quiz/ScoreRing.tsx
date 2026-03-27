import { motion, useAnimation } from "framer-motion";
import { useEffect } from "react";

type ScoreRingProps = {
  score: number;
  maxScore: number;
  percentage: number;
};

export function ScoreRing({ score, maxScore, percentage }: ScoreRingProps) {
  const controls = useAnimation();

  useEffect(() => {
    controls.start({
      strokeDashoffset: 100 - percentage,
      transition: { duration: 1.5, ease: "easeOut" }
    });
  }, [percentage, controls]);

  return (
    <div className="relative mx-auto flex h-48 w-48 items-center justify-center">
      {/* Background glowing blur */}
      <div className="absolute inset-0 rounded-full bg-primary-500/20 blur-3xl" />
      
      <svg className="absolute inset-0 h-full w-full -rotate-90 transform" viewBox="0 0 36 36">
        {/* Background track */}
        <path
          className="text-slate-800/50"
          strokeDasharray="100, 100"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
        />
        {/* Animated Progress */}
        <motion.path
          className="text-primary-500 drop-shadow-[0_0_10px_rgba(99,102,241,0.5)]"
          initial={{ strokeDashoffset: 100 }}
          animate={controls}
          strokeDasharray="100, 100"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
        />
      </svg>
      
      <div className="relative flex flex-col items-center justify-center rounded-full bg-slate-900/80 backdrop-blur-md h-36 w-36 shadow-inner border border-slate-700/50 z-10">
        <p className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-accent-blue drop-shadow-lg">
          {score}
          <span className="text-2xl text-slate-500 font-medium">/{maxScore}</span>
        </p>
        <p className="mt-1 text-sm font-semibold tracking-wide text-primary-300">{percentage}%</p>
      </div>
    </div>
  );
}
