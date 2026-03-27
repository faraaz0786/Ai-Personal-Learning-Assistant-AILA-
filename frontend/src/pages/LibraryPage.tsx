import { BookOpen, Sparkles } from "lucide-react";
import { LibraryList } from "../components/library/LibraryList";
import { motion } from "framer-motion";

export function LibraryPage() {
  return (
    <div className="max-w-5xl mx-auto py-8 px-4 space-y-12">
      {/* Editorial Header */}
      <section className="text-center space-y-4">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#f5f1eb] border border-[#e8e2d8] text-primary-600 text-[10px] font-bold uppercase tracking-[0.2em] mx-auto"
        >
          <Sparkles size={12} className="text-primary-400" />
          <span>Your Intellectual Legacy</span>
        </motion.div>
        
        <h1 className="text-4xl md:text-5xl font-editorial font-bold text-[#3e3a36] tracking-tight">
          The Scholar's <span className="text-primary-500 italic">Library</span>
        </h1>
        
        <p className="max-w-2xl mx-auto text-lg text-[#6b645d] font-serif leading-relaxed opacity-80">
          A definitive collection of your academic inquiries, synthesized insights, 
          and the progression of your intellectual journey.
        </p>
      </section>

      <div className="grid gap-12 lg:grid-cols-[1fr_300px]">
        {/* Main List */}
        <div className="space-y-8">
          <LibraryList />
        </div>

        {/* Sidebar Info */}
        <div className="hidden lg:block space-y-8">
          <div className="scholarly-card p-6 bg-[#fdfaf6] border border-[#e8e2d8]">
            <h3 className="text-sm font-bold text-primary-500 uppercase tracking-widest mb-4">Library Stats</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-[#6b645d] font-serif">Total Volumes</span>
                <span className="font-bold text-[#3e3a36]">--</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-[#6b645d] font-serif">Last Entry</span>
                <span className="font-bold text-[#3e3a36]">Today</span>
              </div>
            </div>
          </div>
          
          <div className="p-6 rounded-2xl bg-primary-500 text-white shadow-lg space-y-4">
            <BookOpen className="w-8 h-8 opacity-50" />
            <h4 className="font-serif text-xl font-bold leading-tight">Master your archives.</h4>
            <p className="text-xs text-primary-50 opacity-80 leading-relaxed">
              Every topic you explore is preserved here. Review them periodically to 
              ensure long-term retention of core concepts.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
