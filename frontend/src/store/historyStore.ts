import { create } from "zustand";
import { persist } from "zustand/middleware";

export type HistoryItem = {
  id: string;
  topic: string;
  timestamp: string;
};

type HistoryState = {
  items: HistoryItem[];
  addHistoryItem: (topic: string) => void;
  clearHistory: () => void;
};

export const useHistoryStore = create<HistoryState>()(
  persist(
    (set) => ({
      items: [],
      addHistoryItem: (topic) => 
        set((state) => ({
          items: [
            { 
              id: Math.random().toString(36).substring(7), 
              topic, 
              timestamp: new Date().toISOString() 
            }, 
            ...state.items.slice(0, 9) // keep last 10
          ]
        })),
      clearHistory: () => set({ items: [] }),
    }),
    {
      name: "aila-history-storage",
    }
  )
);
