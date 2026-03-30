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
    // Keep ready: false if it fails, so we can show an error
  });

  useEffect(() => {
    if (sessionId) {
      setReady(true);
      return;
    }
    
    createSessionMutation.mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (createSessionMutation.isError) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center space-y-4">
        <div className="text-red-500 text-4xl">⚠️</div>
        <h2 className="text-xl font-bold">Service Not Ready</h2>
        <p className="text-gray-500 max-w-sm">
          We couldn't establish a secure learning session. This usually happens if the backend is still waking up.
        </p>
        {(createSessionMutation.error as any)?.details && (
          <div className="mt-4 p-3 bg-red-50 border border-red-100 rounded text-xs text-red-800 font-mono max-w-lg break-all">
            Diagnostic: {(createSessionMutation.error as any).details}
          </div>
        )}
        <button 
          onClick={() => createSessionMutation.mutate()}
          className="px-6 py-2 bg-black text-white rounded-full hover:bg-gray-800 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!ready || createSessionMutation.isPending) {
    return (
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        <div className="flex items-center space-x-2 animate-pulse mb-8">
          <div className="w-8 h-8 bg-gray-200 rounded-full" />
          <div className="h-4 w-32 bg-gray-200 rounded" />
        </div>
        <SkeletonCard lines={3} />
        <SkeletonCard lines={5} />
      </div>
    );
  }

  return <>{children}</>;
}
