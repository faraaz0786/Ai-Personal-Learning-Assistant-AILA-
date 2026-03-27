import { apiClient } from "./client";
import type { SessionResponse } from "../types/api";

export async function createSession() {
  try {
    const response = await apiClient.post<SessionResponse>("/sessions");
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (createSession):", error.response?.data || error.message);
    throw error;
  }
}

export async function getSession(sessionId: string) {
  try {
    const response = await apiClient.get<SessionResponse>(`/sessions/${sessionId}`);
    return response.data;
  } catch (error: any) {
    console.error(`API ERROR (getSession ${sessionId}):`, error.response?.data || error.message);
    throw error;
  }
}
