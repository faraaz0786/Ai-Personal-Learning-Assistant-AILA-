import { apiClient } from "./client";

export type LibraryItem = {
  id: string;
  topic: string;
  summary: string;
  created_at: string;
  last_accessed: string | null;
};

export type LibraryResponse = {
  items: LibraryItem[];
  total_count: number;
};

export async function getLibrary(limit: number = 100, offset: number = 0) {
  try {
    const response = await apiClient.get<LibraryResponse>("/library", {
      params: { limit, offset }
    });
    return response.data;
  } catch (error: any) {
    console.error("API ERROR (getLibrary):", error.response?.data || error.message);
    throw error;
  }
}
