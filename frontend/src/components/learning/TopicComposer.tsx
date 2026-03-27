import type { ExplainRequest } from "../../types/api";
import { Button } from "../atoms/Button";
import { Input } from "../atoms/Input";
import { Select } from "../atoms/Select";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, ArrowRight, Settings, Command } from "lucide-react";

type TopicComposerProps = {
  topic: string;
  subject: ExplainRequest["subject"];
  validationMessage: string;
  loading: boolean;
  onTopicChange: (value: string) => void;
  onSubjectChange: (value: ExplainRequest["subject"]) => void;
  onSubmit: () => void;
};

export function TopicComposer({
  topic,
  subject,
  validationMessage,
  loading,
  onTopicChange,
  onSubjectChange,
  onSubmit
}: TopicComposerProps) {
  return (
    <div className="w-full relative px-6 py-4">
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative max-w-4xl mx-auto"
      >
        {/* Validation Popover - Adjusted position */}
        <AnimatePresence>
          {validationMessage && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="absolute -top-12 left-6 px-4 py-2 bg-red-50 text-red-600 text-xs font-bold border border-red-100 rounded-lg shadow-sm flex items-center gap-2 z-20"
            >
              <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
              {validationMessage}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-primary-500/20 to-secondary-500/10 rounded-[2rem] blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200" />
          
          <div className="relative flex items-center bg-white border border-surface-border rounded-full p-2 pl-6 shadow-academic hover:shadow-academic-hover focus-within:shadow-academic-hover transition-all duration-500">
            <Command size={16} className="text-secondary-muted mr-4" strokeWidth={2.5} />
            
            <Input
              className="flex-1 border-none focus:ring-0 text-base bg-transparent p-0 placeholder:text-secondary-muted/60 font-medium h-12"
              placeholder="Enter a scholarly enquiry... (e.g. 'Thermodynamics in biological systems')"
              value={topic}
              onChange={(event) => onTopicChange(event.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onSubmit()}
              maxLength={500}
              autoFocus
            />

            <div className="flex items-center gap-3 pr-2">
              <div className="hidden sm:flex items-center gap-2 px-3 h-10 rounded-full bg-background-alt/50 border border-surface-border group/select transition-colors hover:border-primary-300">
                <Settings size={14} className="text-secondary-muted group-hover/select:text-primary-500 transition-colors" />
                <Select
                  value={subject}
                  onChange={(event) => onSubjectChange(event.target.value as ExplainRequest["subject"])}
                  className="bg-transparent border-none focus:ring-0 text-[10px] font-bold uppercase tracking-widest text-secondary-muted group-hover/select:text-primary-600 cursor-pointer h-full py-0 pl-1"
                >
                  <option>General</option>
                  <option>Science</option>
                  <option>Technology</option>
                  <option>Mathematics</option>
                  <option>History</option>
                  <option>Humanities</option>
                </Select>
              </div>

              <Button 
                size="sm"
                className="rounded-full w-12 h-12 p-0 flex-shrink-0 bg-primary-500 hover:bg-primary-600 text-white shadow-soft transition-all active:scale-[0.95] flex items-center justify-center" 
                onClick={onSubmit} 
                disabled={loading}
              >
                {loading ? (
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                    <Sparkles size={20} />
                  </motion.div>
                ) : (
                  <ArrowRight size={20} strokeWidth={2.5} />
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Hints / Keyboard shortcuts */}
        <div className="flex justify-center gap-8 mt-4">
          <div className="flex items-center gap-2 text-[10px] text-secondary-muted font-bold tracking-widest uppercase opacity-60">
            <span className="px-1.5 py-0.5 rounded border border-surface-border bg-white text-[9px]">ENTER</span>
            <span>Enquire</span>
          </div>
          <div className="flex items-center gap-2 text-[10px] text-secondary-muted font-bold tracking-widest uppercase opacity-60">
             <span className="px-1.5 py-0.5 rounded border border-surface-border bg-white text-[9px]">/</span>
             <span>Commands</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
