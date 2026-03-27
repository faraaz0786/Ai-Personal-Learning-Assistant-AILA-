import { useState } from "react";
import type { ExplainResponse } from "../../types/api";
import { Button } from "../atoms/Button";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Copy, Check } from "lucide-react";

type SummaryCardProps = {
  response: ExplainResponse | null;
};

export function SummaryCard({ response }: SummaryCardProps) {
  const [copied, setCopied] = useState(false);
  const wordCount = response?.summary.split(/\s+/).filter(Boolean).length ?? 0;

  const handleCopy = async () => {
    if (!response?.summary) return;
    try {
      await navigator.clipboard.writeText(response.summary);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
  };

  if (!response) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} 
      animate={{ opacity: 1, y: 0 }} 
      transition={{ delay: 0.3 }}
      className="scholarly-card p-10 space-y-8 bg-background-alt/30"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-white border border-surface-border flex items-center justify-center text-primary-500 shadow-sm">
            <FileText size={20} />
          </div>
          <h3 className="text-xl font-editorial font-bold text-surface-text-primary tracking-tight">Executive Summary</h3>
        </div>
        <div className="px-3 py-1 bg-white border border-surface-border rounded-full text-[9px] font-bold uppercase tracking-widest text-secondary-muted">
          {wordCount} Words
        </div>
      </div>

      <div className="relative group">
        <div className="absolute -left-10 top-0 text-6xl font-editorial text-primary-500/10 leading-none select-none">
          “
        </div>
        <p className="text-surface-text-primary text-xl leading-relaxed font-editorial italic text-justify opacity-90">
          {response.summary}
        </p>
        <div className="absolute -right-4 bottom-0 text-6xl font-editorial text-primary-500/10 leading-none select-none">
          ”
        </div>
      </div>
      
      <div className="flex items-center justify-end pt-8 border-t border-surface-border border-dashed">
        <Button 
          variant="outline"
          size="sm"
          className="rounded-xl h-10 px-6 flex items-center gap-3 border-surface-border hover:border-primary-300 hover:text-primary-600 transition-all bg-white shadow-soft" 
          onClick={handleCopy}
        >
          <AnimatePresence mode="wait">
            {copied ? (
              <motion.div
                key="check"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.5 }}
                className="flex items-center gap-2 text-green-600 font-bold text-xs"
              >
                <Check size={14} />
                <span>Synchronized to Library</span>
              </motion.div>
            ) : (
              <motion.div
                key="copy"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.5 }}
                className="flex items-center gap-2 font-bold text-xs"
              >
                <Copy size={14} />
                <span>Capture Excerpt</span>
              </motion.div>
            )}
          </AnimatePresence>
        </Button>
      </div>
    </motion.div>
  );
}
