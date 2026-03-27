import { create } from "zustand";
import { persist } from "zustand/middleware";

type UserState = {
  balance: number;
  level: string;
  enquiriesCount: number;
  progress: number;
  currentInsight: {
    tip: string;
    focus_area: string;
    recommendation: string;
  } | null;
  addPoints: (amount: number) => void;
  incrementEnquiries: () => void;
  updateProgress: (value: number) => void;
  setInsight: (insight: UserState["currentInsight"]) => void;
};

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      balance: 1250,
      level: "Scholar",
      enquiriesCount: 0,
      progress: 0,
      currentInsight: null,
      addPoints: (amount) => set((state) => ({ balance: state.balance + amount })),
      incrementEnquiries: () => set((state) => ({ enquiriesCount: state.enquiriesCount + 1 })),
      updateProgress: (value) => set({ progress: value }),
      setInsight: (insight) => set({ currentInsight: insight }),
    }),
    {
      name: "aila-user-storage",
    }
  )
);
