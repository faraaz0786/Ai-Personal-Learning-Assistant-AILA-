import { apiFetch } from "../lib/api";

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
    const response = await apiFetch(`/library?limit=${limit}&offset=${offset}`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return await response.json() as LibraryResponse;
  } catch (error: any) {
    console.error("API ERROR (getLibrary):", error.message);
    throw error;
  }
}
