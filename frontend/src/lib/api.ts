// Centralized API configuration for AILA
export const BASE_URL = import.meta.env.VITE_API_URL!;

/**
 * Standardized fetch wrapper for backend communication.
 * Automatically handles JSON headers and standardizes the base URL.
 */
export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  // Ensure the endpoint starts with a slash
  const url = endpoint.startsWith("/") ? `${BASE_URL}${endpoint}` : `${BASE_URL}/${endpoint}`;
  
  return fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {})
    }
  });
};
