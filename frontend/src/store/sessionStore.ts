import { create } from "zustand";

type SessionState = {
  sessionId: string | null;
  ready: boolean;
  setSessionId: (sessionId: string) => void;
  setReady: (ready: boolean) => void;
};

export const useSessionStore = create<SessionState>((set) => ({
  sessionId: null,
  ready: false,
  setSessionId: (sessionId) => set({ sessionId }),
  setReady: (ready) => set({ ready })
}));
