import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, Search, Clock, ChevronRight } from "lucide-react";
import { getLibrary } from "../../api/library";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "../atoms/Button";
import { Input } from "../atoms/Input";

export const LibraryList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  
  const { data, isLoading, error } = useQuery({
    queryKey: ["scholar-library"],
    queryFn: () => getLibrary(),
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  const filteredItems = data?.items.filter(item => 
    item.topic.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.summary.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="scholarly-card p-4 animate-pulse bg-[#f5f1eb] h-24" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6b645d]" />
        <Input
          placeholder="Search your library..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="space-y-4">
        <AnimatePresence>
          {filteredItems.map((item) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="scholarly-card p-5 group hover:border-primary-500 transition-colors cursor-pointer"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <BookOpen className="w-4 h-4 text-primary-500" />
                    <h4 className="font-serif text-lg text-[#3e3a36] group-hover:text-primary-500 transition-colors">
                      {item.topic}
                    </h4>
                  </div>
                  <p className="text-sm text-[#6b645d] line-clamp-2 leading-relaxed mb-3">
                    {item.summary}
                  </p>
                  <div className="flex items-center gap-3 text-[10px] text-[#a1a1aa] font-medium uppercase tracking-tighter">
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      <span>{new Date(item.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity">
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {filteredItems.length === 0 && (
          <div className="text-center py-12 bg-[#fdfaf6] rounded-xl border-2 border-dashed border-[#e8e2d8]">
            <BookOpen className="w-10 h-10 text-[#e8e2d8] mx-auto mb-3" />
            <p className="text-[#6b645d] font-serif italic">
              No entries found in your scholarly archives.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
