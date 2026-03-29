export const BASE_URL = import.meta.env.VITE_API_URL!;

export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  // Ensure leading slash ONLY (no trailing slash enforcement)
  const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${path}`;

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