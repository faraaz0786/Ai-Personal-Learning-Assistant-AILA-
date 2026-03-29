export const BASE_URL = import.meta.env.VITE_API_URL!;

export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  // Normalize endpoint: ensure leading slash
  let path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  // Normalize endpoint: ensure trailing slash (FastAPI consistency)
  if (!path.endsWith("/")) {
    path = `${path}/`;
  }

  const url = `${BASE_URL}${path}`;
  const method = options?.method || "GET";

  // Only add Content-Type for POST/PUT requests with a body to minimize preflights
  const headers: Record<string, string> = {
    ...(options?.headers as Record<string, string> || {}),
  };

  if (method !== "GET" && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  return fetch(url, {
    ...options,
    method,
    credentials: "include",
    headers,
  });
};



