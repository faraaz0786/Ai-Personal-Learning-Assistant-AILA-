export const BASE_URL = import.meta.env.VITE_API_URL!;

export const apiFetch = async (endpoint: string, options?: RequestInit) => {
  const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${path}`;

  const method = options?.method || "GET";

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
