import { apiClient } from "./client";
import type {
  DashboardSummary,
  ProgressHistoryItem,
  ProgressRecommendation,
  ProgressSummary,
} from "../types/api";

export async function getProgressSummary() {
  try {
    const response = await apiClient.get<ProgressSummary>("/progress/summary");
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getProgressSummary):", error.response?.data || error.message);
    throw error;
  }
}

export async function getDashboardSummary() {
  try {
    const response = await apiClient.get<DashboardSummary>("/progress/dashboard");
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getDashboardSummary):", error.response?.data || error.message);
    throw error;
  }
}

export async function getProgressHistory() {
  try {
    const response = await apiClient.get<ProgressHistoryItem[]>("/progress/history");
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getProgressHistory):", error.response?.data || error.message);
    throw error;
  }
}

export async function getProgressRecommendations() {
  try {
    const response = await apiClient.get<ProgressRecommendation[]>(
      "/progress/recommendations"
    );
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getProgressRecommendations):", error.response?.data || error.message);
    throw error;
  }
}
