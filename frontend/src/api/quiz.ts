import { apiClient } from "./client";
import type { QuizAttemptRequest, QuizAttemptResponse, QuizResponse } from "../types/api";

export async function getQuiz(quizId: string) {
  try {
    const response = await apiClient.get<QuizResponse>(`/quizzes/${quizId}`);
    return response.data;
  } catch (error: any) {
    console.error(`API ERROR (getQuiz ${quizId}):`, error.response?.data || error.message);
    throw error;
  }
}

export async function submitQuizAttempt(quizId: string, payload: QuizAttemptRequest) {
  try {
    const response = await apiClient.post<QuizAttemptResponse>(
      `/quizzes/${quizId}/attempts`,
      payload
    );
    return response.data;
  } catch (error: any) {
    console.error(`API ERROR (submitQuizAttempt ${quizId}):`, error.response?.data || error.message);
    throw error;
  }
}
