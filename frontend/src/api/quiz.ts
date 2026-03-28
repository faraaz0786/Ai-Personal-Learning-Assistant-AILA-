import { apiFetch } from "../lib/api";
import type { QuizAttemptRequest, QuizAttemptResponse, QuizResponse } from "../types/api";

export async function getQuiz(quizId: string) {
  try {
    const response = await apiFetch(`/quizzes/${quizId}`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as QuizResponse;
  } catch (error: any) {
    console.error(`API ERROR (getQuiz ${quizId}):`, error.message);
    throw error;
  }
}

export async function submitQuizAttempt(quizId: string, payload: QuizAttemptRequest) {
  try {
    const response = await apiFetch(`/quizzes/${quizId}/attempts`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as QuizAttemptResponse;
  } catch (error: any) {
    console.error(`API ERROR (submitQuizAttempt ${quizId}):`, error.message);
    throw error;
  }
}
