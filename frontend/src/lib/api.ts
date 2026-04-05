/* ===== API Client for Loteca Mind Backend ===== */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

// 🔴 Keep-Alive: Pinga o Render a cada 14 minutos para ele não dormir
// Garante que webhooks da Kiwify nunca sejam perdidos
if (typeof window !== "undefined") {
  const pingRender = () => fetch(`${API_BASE}/health`).catch(() => {});
  pingRender(); // Pinga imediatamente ao carregar qualquer página
  setInterval(pingRender, 14 * 60 * 1000); // Depois a cada 14 minutos
}

export const api = {
  matches: {
    list: () => fetchAPI<import("./types").MatchesResponse>("/api/matches"),
    get: (id: number) => fetchAPI<import("./types").MatchData>(`/api/matches/${id}`),
  },
  predictions: {
    analyze: (budget = 49.9) =>
      fetchAPI<import("./types").LotecaPrediction>(`/api/predictions/analyze?target_budget=${budget}`, {
        method: "POST",
      }),
    latest: () => fetchAPI<import("./types").LotecaPrediction>("/api/predictions/latest"),
    get: (matchId: number) =>
      fetchAPI<{ fusion: import("./types").FusionResult; suggestion: import("./types").TicketSuggestion }>(
        `/api/predictions/${matchId}`
      ),
  },
  leaderboard: {
    get: () => fetchAPI<import("./types").LeaderboardResponse>("/api/leaderboard"),
    badges: (userId: string) =>
      fetchAPI<{ user_id: string; badges: import("./types").Badge[] }>(`/api/leaderboard/badges/${userId}`),
  },
  admin: {
    updateConcurso: (round_number: number, matches: [string, string][]) =>
      fetchAPI<{ status: string; message: string }>("/api/admin/concurso", {
        method: "POST",
        body: JSON.stringify({ round_number, matches }),
      }),
  },
  auth: {
    checkVip: (email: string) => fetchAPI<{ email: string; is_vip: boolean }>(`/api/auth/check-vip/${encodeURIComponent(email)}`),
  },
};
