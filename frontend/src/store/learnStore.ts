import { create } from "zustand";
import type { ExplainResponse } from "../types/api";

type LearnState = {
  topic: string;
  subject: "Mathematics" | "Science" | "History" | "Technology" | "General";
  response: ExplainResponse | null;
  setTopic: (topic: string) => void;
  setSubject: (subject: LearnState["subject"]) => void;
  setResponse: (response: ExplainResponse) => void;
  reset: () => void;
};

const initialState = {
  topic: "",
  subject: "General" as const,
  response: null,
};

export const useLearnStore = create<LearnState>((set) => ({
  ...initialState,
  setTopic: (topic) => set({ topic }),
  setSubject: (subject) => set({ subject }),
  setResponse: (response) => set({ response }),
  reset: () => set(initialState),
}));
