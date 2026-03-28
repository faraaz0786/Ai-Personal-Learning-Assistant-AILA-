import { apiFetch } from "../lib/api";

export type MentorTip = {
  tip: string;
  focus_area: string;
  recommendation: string;
};

export async function getMentorTip() {
  try {
    const response = await apiFetch("/insights/mentor-tip");
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as MentorTip;
  } catch (error: any) {
    console.error("API ERROR (getMentorTip):", error.message);
    throw error;
  }
}
