const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const url = `${API_URL}${path}`;
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (res.status === 429) {
      const body = await res.json();
      return { data: null, error: body.detail || "Rate limit exceeded" };
    }

    if (!res.ok) {
      return { data: null, error: `HTTP ${res.status}` };
    }

    const data = await res.json();
    return { data: data as T, error: null };
  } catch (err) {
    return { data: null, error: err instanceof Error ? err.message : "Network error" };
  }
}

export async function apiGet<T>(path: string): Promise<ApiResponse<T>> {
  return apiFetch<T>(path);
}

export async function apiPost<T>(path: string, body: unknown): Promise<ApiResponse<T>> {
  return apiFetch<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function checkHealth(): Promise<{ online: boolean; latencyMs: number }> {
  try {
    const start = performance.now();
    const res = await fetch(`${API_URL}/health`);
    const latencyMs = Math.round(performance.now() - start);
    return { online: res.ok, latencyMs };
  } catch {
    return { online: false, latencyMs: 0 };
  }
}
