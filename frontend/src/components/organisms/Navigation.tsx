import { Link, useLocation } from "react-router-dom";
import { LogIn, Brain, Zap, Shield, Sparkles } from "lucide-react";
import { useSessionStore } from "../../store/sessionStore";
import { motion } from "framer-motion";
import { Button } from "../atoms/Button";

export function Navigation() {
  const sessionId = useSessionStore((state) => state.sessionId);
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 w-full bg-white/70 backdrop-blur-xl border-b border-surface-border transition-all duration-300">
      <div className="max-w-7xl mx-auto px-6 lg:px-12 h-24 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-4 group group-hover:no-underline">
            <div className="relative">
              <div className="w-12 h-12 rounded-[18px] bg-primary-600 flex items-center justify-center shadow-xl shadow-primary-200 group-hover:rotate-6 transition-all duration-500">
                <Brain className="text-white w-6 h-6" />
              </div>
              <motion.div 
                animate={{ scale: [1, 1.2, 1] }} 
                transition={{ repeat: Infinity, duration: 2 }}
                className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-white border-4 border-white shadow-sm flex items-center justify-center overflow-hidden"
              >
                <div className="w-full h-full bg-emerald-500" />
              </motion.div>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-black text-slate-800 tracking-tight leading-none group-hover:text-primary-600 transition-colors">
                AILA
              </span>
              <div className="flex items-center gap-2 mt-1.5">
                <Sparkles size={10} className="text-primary-500" />
                <span className="text-[10px] uppercase tracking-[0.2em] font-black text-slate-400">
                  Intelligent Workspace
                </span>
              </div>
            </div>
          </Link>
        </div>

        <nav className="hidden md:flex items-center bg-slate-50 border border-surface-border p-1.5 rounded-2xl gap-1">
          {sessionId && (
            <>
              <Link 
                to="/learn" 
                className={`px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all duration-300 ${
                  location.pathname === '/learn' 
                    ? 'bg-white text-primary-600 shadow-sm border border-surface-border' 
                    : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                Learn
              </Link>
              <Link 
                to="/quiz" 
                className={`px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all duration-300 ${
                  location.pathname === '/quiz' 
                    ? 'bg-white text-primary-600 shadow-sm border border-surface-border' 
                    : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                Assessments
              </Link>
            </>
          )}
        </nav>

        <div className="flex items-center gap-6">
          <div className="hidden lg:flex items-center gap-4 text-[11px] font-black uppercase tracking-widest text-slate-400">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-full border border-surface-border">
              <Zap size={12} className="text-amber-500" />
              <span>Core: v2.4</span>
            </div>
          </div>

          <div className="h-8 w-px bg-surface-border hidden sm:block" />

          <div className="flex items-center gap-4">
            {sessionId ? (
              <div className="flex items-center gap-4 group cursor-pointer">
                <div className="flex flex-col items-end hidden sm:flex">
                  <span className="text-sm font-black text-slate-800 leading-none">Power User</span>
                  <span className="text-[10px] font-bold text-emerald-500 uppercase tracking-wider mt-1">Status: Active</span>
                </div>
                <div className="w-11 h-11 rounded-2xl bg-white border border-surface-border flex items-center justify-center text-primary-600 font-black text-sm shadow-soft group-hover:border-primary-300 group-hover:shadow-primary-100 transition-all duration-300">
                  U
                </div>
              </div>
            ) : (
              <Link to="/login">
                <Button variant="outline" size="sm" className="rounded-xl font-black uppercase tracking-widest text-[10px] h-11 px-6">
                  <LogIn size={16} className="mr-2" />
                  Initialize
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
