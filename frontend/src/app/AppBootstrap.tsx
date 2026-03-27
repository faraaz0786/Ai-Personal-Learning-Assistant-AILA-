import { ReactNode, useEffect } from "react";

import { useMutation } from "@tanstack/react-query";

import { createSession } from "../api/session";
import { SkeletonCard } from "../components/feedback/SkeletonCard";
import { useSessionStore } from "../store/sessionStore";

type AppBootstrapProps = {
  children: ReactNode;
};

export function AppBootstrap({ children }: AppBootstrapProps) {
  const sessionId = useSessionStore((state) => state.sessionId);
  const ready = useSessionStore((state) => state.ready);
  const setSessionId = useSessionStore((state) => state.setSessionId);
  const setReady = useSessionStore((state) => state.setReady);

  const createSessionMutation = useMutation({
    mutationFn: createSession,
    onSuccess: (session) => {
      setSessionId(session.id);
      setReady(true);
    },
    onError: () => {
      setReady(true);
    }
  });

  useEffect(() => {
    if (sessionId) {
      if (!ready) setReady(true);
      return;
    }
    
    // Only run this ONCE.
    createSessionMutation.mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!ready) {
    return (
      <div className="space-y-6">
        <SkeletonCard lines={3} />
        <SkeletonCard lines={5} />
      </div>
    );
  }

  return <>{children}</>;
}
