import { apiFetch } from "../lib/api";
import type {
  ExplainRequest,
  ExplainResponse,
  QuizRequest,
  QuizResponse,
  TopicListItem,
} from "../types/api";

export async function explainTopic(payload: ExplainRequest) {
  try {
    const response = await apiFetch("/learn/explain", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as ExplainResponse;
  } catch (error: any) {
    console.error("API ERROR (explainTopic):", error.message);
    throw error;
  }
}

export async function generateQuiz(payload: QuizRequest) {
  try {
    const response = await apiFetch("/learn/quiz", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as QuizResponse;
  } catch (error: any) {
    console.error("API ERROR (generateQuiz):", error.message);
    throw error;
  }
}

export async function getTopics() {
  try {
    const response = await apiFetch("/learn/topics");
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as TopicListItem[];
  } catch (error: any) {
    console.error("API ERROR (getTopics):", error.message);
    throw error;
  }
}
