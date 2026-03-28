import { apiFetch } from "../lib/api";
import type {
  DashboardSummary,
  ProgressHistoryItem,
  ProgressRecommendation,
  ProgressSummary,
} from "../types/api";

export async function getProgressSummary() {
  try {
    const response = await apiFetch("/progress/summary");
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as ProgressSummary;
  } catch (error: any) {
    console.error("API ERROR (getProgressSummary):", error.message);
    throw error;
  }
}

export async function getDashboardSummary() {
  try {
    const response = await apiFetch("/progress/dashboard");
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as DashboardSummary;
  } catch (error: any) {
    console.error("API ERROR (getDashboardSummary):", error.message);
    throw error;
  }
}

export async function getProgressHistory() {
  try {
    const response = await apiFetch("/progress/history");
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as ProgressHistoryItem[];
  } catch (error: any) {
    console.error("API ERROR (getProgressHistory):", error.message);
    throw error;
  }
}

export async function getProgressRecommendations() {
  try {
    const response = await apiFetch("/progress/recommendations");
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as ProgressRecommendation[];
  } catch (error: any) {
    console.error("API ERROR (getProgressRecommendations):", error.message);
    throw error;
  }
}
