import { apiClient } from "./client";

export type MentorTip = {
  tip: string;
  focus_area: string;
  recommendation: string;
};

export async function getMentorTip() {
  try {
    const response = await apiClient.get<MentorTip>("/insights/mentor-tip");
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getMentorTip):", error.response?.data || error.message);
    throw error;
  }
}
