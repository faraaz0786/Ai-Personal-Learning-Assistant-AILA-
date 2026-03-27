import { Button } from "../atoms/Button";
import { Card } from "../molecules/Card";
import { Brain, Download, Lock, CheckCircle2, Layout } from "lucide-react";
import { motion } from "framer-motion";

type LearningSidePanelProps = {
  canGenerateQuiz: boolean;
  loading: boolean;
  errorMessage: string | null;
  onGenerateQuiz: () => void;
};

export function LearningSidePanel({
  canGenerateQuiz,
  loading,
  errorMessage,
  onGenerateQuiz,
}: LearningSidePanelProps) {
  return (
    <Card title="Workspace Tools" className="bg-white border-surface-border shadow-soft">
      <div className="flex flex-col gap-6">
        {errorMessage && (
          <div className="text-sm text-red-600 bg-red-50 p-4 rounded-2xl border border-red-100 font-bold">
            {errorMessage}
          </div>
        )}
        
        <div className="space-y-4">
          <Button 
            size="lg"
            className="w-full h-14 flex items-center justify-center gap-3 shadow-soft text-base font-black rounded-2xl" 
            onClick={onGenerateQuiz} 
            disabled={!canGenerateQuiz || loading}
          >
            {loading ? (
              <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2, ease: "linear" }}>
                <Brain size={20} />
              </motion.div>
            ) : (
              <Brain size={20} />
            )}
            {loading ? "Generating Quiz..." : "Start Mastery Quiz"}
          </Button>
  
          {!canGenerateQuiz && (
            <div className="flex items-start gap-3 text-sm text-slate-500 bg-slate-50 p-4 rounded-2xl border border-surface-border">
              <Lock size={18} className="shrink-0 text-slate-300" />
              <p className="font-medium leading-relaxed">
                Complete the explanation above to unlock your personalized mastery quiz.
              </p>
            </div>
          )}
        </div>
 
        <div className="h-px w-full bg-surface-border" />
 
        <div className="space-y-3">
          <h4 className="text-xs font-black text-slate-400 uppercase tracking-widest px-2">Knowledge Extras</h4>
          <Button variant="ghost" className="w-full h-12 flex items-center justify-start gap-3 text-slate-400 px-4 rounded-xl" disabled>
            <Download size={18} />
            <span className="font-bold">Export Learning PDF</span>
          </Button>
          <Button variant="ghost" className="w-full h-12 flex items-center justify-start gap-3 text-slate-400 px-4 rounded-xl" disabled>
            <Layout size={18} />
            <span className="font-bold">Flashcard Mode</span>
          </Button>
        </div>
        
        {canGenerateQuiz && (
          <div className="flex items-center gap-3 px-4 py-3 bg-primary-50 rounded-2xl border border-primary-100/50">
            <CheckCircle2 size={16} className="text-primary-600" />
            <span className="text-xs font-black text-primary-600 uppercase tracking-wider">Topic Fully Indexed</span>
          </div>
        )}
      </div>
    </Card>
  );
}
