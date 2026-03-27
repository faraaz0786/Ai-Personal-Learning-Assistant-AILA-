import { Link } from "react-router-dom";
import { Button } from "../components/atoms/Button";
import { Sparkles, Brain, BookMarked, GraduationCap, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";

export function HomePage() {
  return (
    <div className="max-w-6xl mx-auto space-y-16 py-8">
      {/* Editorial Hero Section */}
      <section className="relative overflow-hidden rounded-[40px] bg-white border border-surface-border p-12 md:p-20 shadow-soft group">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-primary-500/5 rounded-full blur-[120px] -translate-y-1/2 translate-x-1/2 group-hover:bg-primary-500/10 transition-colors duration-700" />
        
        <div className="relative z-10 max-w-3xl space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-background-alt border border-surface-border text-primary-600 text-[10px] font-bold uppercase tracking-[0.2em]">
            <Sparkles size={12} className="text-primary-400" />
            <span>Academic Excellence Redefined</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-editorial font-bold text-surface-text-primary tracking-tight leading-[1.05]">
            Illuminating the <br />
            <span className="text-primary-500 italic">path to mastery.</span>
          </h1>
          
          <p className="max-w-xl text-lg text-secondary-muted font-medium leading-relaxed font-serif opacity-80">
            AILA is your personal learning concierge, transforming complex information into 
            structured, scholarly insight through intelligent dialogue and rigorous assessment.
          </p>
          
          <div className="pt-6 flex flex-wrap gap-6">
            <Link to="/learn">
              <Button size="lg" className="rounded-2xl px-10 h-16 text-base font-bold shadow-soft flex items-center gap-2 group/btn">
                Commence Learning
                <ChevronRight size={18} className="group-hover/btn:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="rounded-2xl px-10 h-16 text-base font-bold bg-white border-surface-border hover:border-primary-300">
              Explore Library
            </Button>
          </div>
        </div>
      </section>
      
      {/* Scholarly Pillars */}
      <div className="grid gap-8 md:grid-cols-3">
        {[
          {
            icon: <Brain size={22} />,
            title: "Intellectual Rigor",
            desc: "Deep-dive explanations that unravel the core mechanisms of any discipline."
          },
          {
            icon: <BookMarked size={22} />,
            title: "Curation & Synthesis",
            desc: "Expertly crafted summaries that distill vast knowledge into essential wisdom."
          },
          {
            icon: <GraduationCap size={22} />,
            title: "Validated Mastery",
            desc: "Dynamic assessments designed to verify true comprehension and retention."
          }
        ].map((pillar, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * i }}
            className="scholarly-card p-10 space-y-6 group hover:-translate-y-2 transition-transform duration-500"
          >
            <div className="w-12 h-12 rounded-2xl bg-background-alt border border-surface-border flex items-center justify-center text-primary-500 shadow-sm group-hover:border-primary-200 transition-colors">
              {pillar.icon}
            </div>
            <div className="space-y-3">
              <h3 className="text-xl font-editorial font-bold text-surface-text-primary tracking-tight">
                {pillar.title}
              </h3>
              <p className="text-secondary-muted text-sm font-medium leading-relaxed font-serif opacity-70">
                {pillar.desc}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
