const rawApiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
export const BASE_URL = rawApiUrl.replace(/\/$/, "");

export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  // Ensure we don't have double slashes and endpoint is clean
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${cleanEndpoint}`;

  const method = options?.method || "GET";

  // Clean headers (avoid unnecessary preflight)
  const headers: Record<string, string> = {
    ...(options?.headers as Record<string, string> || {}),
  };

  // Only attach Content-Type when needed
  if (method !== "GET" && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  return fetch(url, {
    ...options,
    method,
    credentials: "include", // 🔥 REQUIRED for cookies
    headers,
  });
};