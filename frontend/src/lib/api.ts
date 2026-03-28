// Centralized API configuration for AILA
export const BASE_URL = import.meta.env.VITE_API_URL!;

/**
 * Standardized fetch wrapper for backend communication.
 * - Ensures correct base URL
 * - Adds credentials (cookies)
 * - Normalizes endpoint paths
 * - Enforces correct HTTP methods for specific endpoints
 */
export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  // 1. Normalize endpoint path
  let normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  // 2. Ensure /api/v1 prefix is enforced if missing
  if (!normalizedEndpoint.startsWith("/api/v1")) {
    normalizedEndpoint = `/api/v1${normalizedEndpoint}`;
  }

  // 3. SAFE Fallback: If endpoint is sessions and no method is provided, default to POST
  // We check for both with and without the prefix for robustness
  const isSessionEndpoint = 
    normalizedEndpoint === "/api/v1/sessions" || 
    normalizedEndpoint === "/sessions";
    
  const method = options?.method || (isSessionEndpoint ? "POST" : "GET");

  const url = `${BASE_URL}${normalizedEndpoint}`;

  // 4. Execute fetch with standardized config
  return fetch(url, {
    ...options,
    method,
    
    // 🔥 CRITICAL: required for cookies/session persistence
    credentials: "include",

    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });
};
