import { apiFetch } from "../lib/api";
import type { SessionResponse } from "../types/api";

export class SessionStatusError extends Error {
  details?: string;
  constructor(message: string, details?: string) {
    super(message);
    this.name = "SessionStatusError";
    this.details = details;
  }
}

export async function createSession() {
  try {
    const response = await apiFetch("/sessions/", { method: "POST" });
    if (!response.ok) {
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json().catch(() => ({}));
            throw new SessionStatusError(
                errorData.message || `HTTP error! status: ${response.status}`,
                errorData.details
            );
        }
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json() as SessionResponse;
  } catch (error: any) {
    console.error("API ERROR (createSession):", error.message);
    throw error;
  }
}

export async function getSession(sessionId: string) {
  try {
    const response = await apiFetch(`/sessions/${sessionId}`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as SessionResponse;
  } catch (error: any) {
    console.error(`API ERROR (getSession ${sessionId}):`, error.message);
    throw error;
  }
}
