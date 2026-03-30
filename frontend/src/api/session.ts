import { apiFetch } from "../lib/api";
import type { SessionResponse } from "../types/api";

export async function createSession() {
  try {
    const response = await apiFetch("/sessions/", { method: "POST" });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
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
