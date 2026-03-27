import type { ExplainResponse } from "../../types/api";
import { motion, Variants } from "framer-motion";
import { BookText, Cog, Lightbulb, Clock, CheckCircle2 } from "lucide-react";

type ExplanationCardProps = {
  response: ExplainResponse | null;
};

const container: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.15 }
  }
};

const item: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", bounce: 0.3, duration: 0.8 } }
};

export function ExplanationCard({ response }: ExplanationCardProps) {
  if (!response) return null;

  return (
    <motion.div 
      variants={container} 
      initial="hidden" 
      animate="show" 
      className="space-y-16"
    >
      {/* Normalized Topic Heading */}
      <motion.div variants={item} className="space-y-2">
        <span className="text-[10px] font-bold text-primary-500 uppercase tracking-widest">Enquiry Topic</span>
        <h2 className="text-4xl font-editorial font-bold text-surface-text-primary tracking-tight">
          {response.normalized_topic}
        </h2>
        <div className="w-12 h-0.5 bg-primary-500/30 rounded-full" />
      </motion.div>

      <motion.section variants={item} className="relative">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-10 h-10 rounded-xl bg-background-alt border border-surface-border flex items-center justify-center text-primary-500 shadow-sm">
            <BookText size={20} />
          </div>
          <h3 className="text-xl font-editorial font-bold text-surface-text-primary tracking-tight">Core Concept</h3>
        </div>
        <div className="pl-14">
          <p className="text-surface-text-secondary text-lg leading-relaxed font-serif italic text-justify opacity-90 first-letter:text-3xl first-letter:font-bold first-letter:text-primary-500 first-letter:float-left first-letter:mr-3 first-letter:mt-1">
            {response.explanation.definition}
          </p>
        </div>
      </motion.section>

      <motion.section variants={item} className="relative">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-10 h-10 rounded-xl bg-background-alt border border-surface-border flex items-center justify-center text-primary-500 shadow-sm">
            <Cog size={20} />
          </div>
          <h3 className="text-xl font-editorial font-bold text-surface-text-primary tracking-tight">Mechanism of Action</h3>
        </div>
        <div className="pl-14">
          <p className="text-surface-text-secondary text-[1.05rem] leading-relaxed font-medium">
            {response.explanation.mechanism}
          </p>
        </div>
      </motion.section>

      <motion.section variants={item} className="relative">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-10 h-10 rounded-xl bg-background-alt border border-surface-border flex items-center justify-center text-primary-500 shadow-sm">
            <Lightbulb size={20} />
          </div>
          <h3 className="text-xl font-editorial font-bold text-surface-text-primary tracking-tight">Scholarly Exemplification</h3>
        </div>
        <div className="ml-14 bg-background-alt/50 p-10 rounded-3xl border border-surface-border shadow-inner-soft relative group">
          <div className="absolute top-0 left-8 px-3 py-1 bg-white border border-surface-border rounded-b-xl text-[9px] font-bold uppercase tracking-widest text-secondary-muted -translate-y-px">
            Case Study
          </div>
          <p className="text-surface-text-primary text-xl leading-relaxed italic font-editorial">
            "{response.explanation.example}"
          </p>
        </div>
      </motion.section>

      {/* Metadata / Trust Bar */}
      <motion.div variants={item} className="flex flex-col sm:flex-row items-center justify-between gap-6 pt-12 border-t border-surface-border border-dashed">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 text-[10px] font-bold text-secondary-muted uppercase tracking-widest">
            <Clock size={12} className="opacity-50" />
            <span>Refined in {response.response_ms}ms</span>
          </div>
          <div className="flex items-center gap-2 text-[10px] font-bold text-green-600 uppercase tracking-widest">
            <CheckCircle2 size={12} className="opacity-70" />
            <span>Scholarly Verified</span>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
