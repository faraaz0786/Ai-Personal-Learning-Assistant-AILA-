import { apiClient } from "./client";
import type {
  ExplainRequest,
  ExplainResponse,
  QuizRequest,
  QuizResponse,
  TopicListItem,
} from "../types/api";

export async function explainTopic(payload: ExplainRequest) {
  try {
    const response = await apiClient.post<ExplainResponse>("/learn/explain", payload);
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (explainTopic):", error.response?.data || error.message);
    throw error;
  }
}

export async function generateQuiz(payload: QuizRequest) {
  try {
    const response = await apiClient.post<QuizResponse>("/learn/quiz", payload);
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (generateQuiz):", error.response?.data || error.message);
    throw error;
  }
}

export async function getTopics() {
  try {
    const response = await apiClient.get<TopicListItem[]>("/learn/topics");
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getTopics):", error.response?.data || error.message);
    throw error;
  }
}
