"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import { api } from "@/lib/api";
import type { LeaderboardEntry } from "@/lib/types";

const TIER_COLORS: Record<string, string> = {
  Master: "#f43f5e",
  Diamond: "#8b5cf6",
  Gold: "#f59e0b",
  Silver: "#94a3b8",
  Bronze: "#b45309",
};

const TIER_ICONS: Record<string, string> = {
  Master: "👑",
  Diamond: "💎",
  Gold: "🥇",
  Silver: "🥈",
  Bronze: "🥉",
};

function RankBadge({ rank }: { rank: number }) {
  if (rank === 1)
    return (
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
        style={{ background: "linear-gradient(135deg, #f59e0b, #f43f5e)", color: "white" }}
      >
        1
      </div>
    );
  if (rank === 2)
    return (
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
        style={{ background: "linear-gradient(135deg, #94a3b8, #64748b)", color: "white" }}
      >
        2
      </div>
    );
  if (rank === 3)
    return (
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
        style={{ background: "linear-gradient(135deg, #b45309, #92400e)", color: "white" }}
      >
        3
      </div>
    );
  return (
    <div
      className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold"
      style={{ background: "var(--bg-elevated)", color: "var(--text-secondary)" }}
    >
      {rank}
    </div>
  );
}

export default function LeaderboardPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [totalUsers, setTotalUsers] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.leaderboard
      .get()
      .then((data) => {
        setEntries(data.entries);
        setTotalUsers(data.total_users);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
      <Navbar />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
        {/* Header */}
        <div className="text-center mb-10" style={{ animation: "fade-in 0.6s ease-out" }}>
          <h1
            className="text-4xl font-bold mb-3"
            style={{ fontFamily: "var(--font-outfit)" }}
          >
            🏆{" "}
            <span className="text-gradient">Global Leaderboard</span>
          </h1>
          <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
            Top estrategistas da Loteca Mind • {totalUsers.toLocaleString()} jogadores
          </p>
        </div>

        {/* Podium (Top 3) */}
        {entries.length >= 3 && (
          <div
            className="grid grid-cols-3 gap-3 mb-8"
            style={{ animation: "slide-up 0.5s ease-out 0.1s backwards" }}
          >
            {[entries[1], entries[0], entries[2]].map((entry, i) => {
              const positions = [2, 1, 3];
              const heights = ["h-36", "h-44", "h-32"];
              const rank = positions[i];
              return (
                <div
                  key={entry.user_id}
                  className={`glass-card flex flex-col items-center justify-center p-4 ${heights[i]}`}
                  style={{
                    borderColor:
                      rank === 1 ? "rgba(245, 158, 11, 0.3)" : "var(--border-subtle)",
                    boxShadow:
                      rank === 1 ? "0 0 30px rgba(245, 158, 11, 0.1)" : "none",
                  }}
                >
                  <div className="text-3xl mb-2">{TIER_ICONS[entry.tier] || "🏅"}</div>
                  <div className="text-xl font-bold mb-1" style={{ color: TIER_COLORS[entry.tier] }}>
                    #{rank}
                  </div>
                  <div
                    className="font-semibold text-sm truncate max-w-full"
                    style={{ color: "var(--text-primary)" }}
                  >
                    {entry.display_name}
                  </div>
                  <div className="text-lg font-bold mt-1" style={{ color: "var(--accent-emerald)" }}>
                    {entry.total_points.toLocaleString()}
                  </div>
                  <div className="text-[0.6rem]" style={{ color: "var(--text-secondary)" }}>
                    {(entry.accuracy_rate * 100).toFixed(0)}% acerto
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Table */}
        <div className="glass-card overflow-hidden">
          <div
            className="grid grid-cols-[60px_1fr_100px_100px_80px] sm:grid-cols-[60px_1fr_120px_120px_100px] gap-2 px-5 py-3 text-[0.7rem] font-semibold"
            style={{
              color: "var(--text-muted)",
              letterSpacing: "0.05em",
              borderBottom: "1px solid var(--border-subtle)",
              background: "var(--bg-secondary)",
            }}
          >
            <span>#</span>
            <span>JOGADOR</span>
            <span className="text-center">PONTOS</span>
            <span className="text-center">ACERTO</span>
            <span className="text-center">TIER</span>
          </div>

          {loading ? (
            <div className="p-8 text-center" style={{ color: "var(--text-muted)" }}>
              Carregando ranking...
            </div>
          ) : (
            entries.map((entry, i) => (
              <div
                key={entry.user_id}
                className="grid grid-cols-[60px_1fr_100px_100px_80px] sm:grid-cols-[60px_1fr_120px_120px_100px] gap-2 px-5 py-4 items-center transition-all duration-200"
                style={{
                  borderBottom: "1px solid var(--border-subtle)",
                  animation: `slide-up 0.4s ease-out ${i * 0.05}s backwards`,
                  background: entry.rank <= 3 ? "rgba(16, 185, 129, 0.03)" : "transparent",
                }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.background = "var(--bg-card-hover)")
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.background =
                    entry.rank <= 3 ? "rgba(16, 185, 129, 0.03)" : "transparent")
                }
              >
                <RankBadge rank={entry.rank} />
                <div>
                  <div className="font-semibold text-sm" style={{ color: "var(--text-primary)" }}>
                    {entry.display_name}
                  </div>
                  <div className="text-[0.65rem] flex items-center gap-1" style={{ color: "var(--text-muted)" }}>
                    {entry.badges_count} badges
                  </div>
                </div>
                <div className="text-center font-bold text-sm" style={{ color: "var(--accent-emerald)" }}>
                  {entry.total_points.toLocaleString()}
                </div>
                <div className="text-center">
                  <div className="progress-bar mx-auto" style={{ width: "80px" }}>
                    <div
                      className="progress-fill"
                      style={{
                        width: `${entry.accuracy_rate * 100}%`,
                        background:
                          entry.accuracy_rate >= 0.65
                            ? "var(--accent-emerald)"
                            : entry.accuracy_rate >= 0.5
                            ? "var(--accent-amber)"
                            : "var(--accent-rose)",
                      }}
                    />
                  </div>
                  <div className="text-[0.6rem] mt-1" style={{ color: "var(--text-secondary)" }}>
                    {(entry.accuracy_rate * 100).toFixed(0)}%
                  </div>
                </div>
                <div className="text-center">
                  <span
                    className="tag text-[0.6rem]"
                    style={{
                      background: `${TIER_COLORS[entry.tier]}20`,
                      color: TIER_COLORS[entry.tier],
                      border: `1px solid ${TIER_COLORS[entry.tier]}40`,
                    }}
                  >
                    {entry.tier}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}
