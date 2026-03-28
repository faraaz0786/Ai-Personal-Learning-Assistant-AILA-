// Centralized API configuration for AILA
export const BASE_URL = import.meta.env.VITE_API_URL!;

/**
 * Standardized fetch wrapper for backend communication.
 * - Ensures correct base URL
 * - Adds credentials (cookies)
 * - Normalizes endpoint paths
 */
export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  // Ensure endpoint starts with /api/v1
  let normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  if (!normalizedEndpoint.startsWith("/api/v1")) {
    normalizedEndpoint = `/api/v1${normalizedEndpoint}`;
  }

  const url = `${BASE_URL}${normalizedEndpoint}`;

  return fetch(url, {
    ...options,

    // 🔥 CRITICAL: required for cookies/session
    credentials: "include",

    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });
};
