"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import { api } from "@/lib/api";
import type { LeaderboardEntry } from "@/lib/types";

function RankBadge({ rank }: { rank: number }) {
  const styles: Record<number, string> = {
    1: "bg-amber-400 text-amber-900 shadow-[0_0_15px_rgba(251,191,36,0.4)]",
    2: "bg-slate-300 text-slate-800 shadow-[0_0_15px_rgba(203,213,225,0.4)]",
    3: "bg-orange-400 text-orange-950 shadow-[0_0_15px_rgba(251,146,60,0.4)]",
  };

  return (
    <div
      className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
        styles[rank] || "bg-[var(--bg-secondary)] text-[var(--text-secondary)]"
      }`}
    >
      {rank}
    </div>
  );
}

function PodiumCard({ entry, rank }: { entry: LeaderboardEntry; rank: number }) {
  const isFirst = rank === 1;
  
  return (
    <div 
      className={`flex flex-col items-center p-6 glass-card relative transition-all duration-500 ${
        isFirst ? "scale-110 z-10 -translate-y-4 border-[var(--accent-emerald)] shadow-glow-emerald" : "scale-95 opacity-90"
      }`}
      style={{ animation: "slide-up 0.5s ease-out backwards" }}
    >
      <div className="absolute -top-4 -left-2 scale-150 transform rotate-12">
        {isFirst ? "👑" : rank === 2 ? "🥈" : "🥉"}
      </div>
      
      <div 
        className={`w-20 h-20 rounded-2xl flex items-center justify-center text-2xl font-bold mb-4 shadow-lg ${
          isFirst ? "bg-gradient-to-br from-amber-300 to-amber-500 text-amber-900" : 
          rank === 2 ? "bg-gradient-to-br from-slate-200 to-slate-400 text-slate-800" :
          "bg-gradient-to-br from-orange-300 to-orange-500 text-orange-900"
        }`}
      >
        {entry.display_name.charAt(0).toUpperCase()}
      </div>
      
      <div className="text-center">
        <h3 className="font-bold text-[var(--text-primary)] mb-1 truncate max-w-[120px]">
          {entry.display_name}
        </h3>
        <div className="text-[var(--accent-emerald)] font-bold text-lg">
          {entry.total_points.toLocaleString()} <span className="text-[0.6rem] font-medium uppercase tracking-tighter">pts</span>
        </div>
        <div className="text-[0.6rem] uppercase font-bold tracking-widest mt-1 px-2 py-0.5 rounded bg-[var(--bg-elevated)] inline-block">
          {entry.tier}
        </div>
      </div>
    </div>
  );
}

export default function LeaderboardPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.leaderboard.get()
      .then(data => setEntries(data.entries))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const top3 = entries.slice(0, 3);
  const rest = entries.slice(3);

  if (loading) {
    return (
      <div className="min-h-screen bg-[var(--bg-primary)]">
        <Navbar />
        <div className="flex items-center justify-center h-[60vh]">
          <div className="w-10 h-10 border-3 border-[var(--accent-emerald)] border-t-transparent rounded-full animate-spin" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg-primary)]">
      <Navbar />

      <main className="max-w-5xl mx-auto px-4 py-12">
        <header className="text-center mb-16" style={{ animation: "fade-in 0.6s ease-out" }}>
          <div className="text-[var(--accent-emerald)] font-bold text-xs uppercase tracking-[0.2em] mb-3">
            Exploração de Performance
          </div>
          <h1 className="text-4xl font-bold mb-4 font-outfit" style={{ color: "var(--text-primary)" }}>
            Global <span className="text-gradient">Leaderboard</span>
          </h1>
          <p className="text-[var(--text-secondary)] text-sm max-w-lg mx-auto leading-relaxed">
            O pódio dos analistas que transformam dados em previsões precisas. 
            Pontue acertando os 14 jogos e ganhe badges exclusivas.
          </p>
        </header>

        {/* Podium */}
        {top3.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-end mb-20 px-8">
            {/* Rank 2 */}
            {top3[1] && <PodiumCard entry={top3[1]} rank={2} />}
            
            {/* Rank 1 */}
            {top3[0] && <PodiumCard entry={top3[0]} rank={1} />}
            
            {/* Rank 3 */}
            {top3[2] && <PodiumCard entry={top3[2]} rank={3} />}
          </div>
        )}

        {/* List Table */}
        <div className="glass-card overflow-hidden" style={{ animation: "slide-up 0.5s ease-out 0.2s backwards" }}>
          <div className="p-6 border-b border-[var(--border-subtle)] flex items-center justify-between">
            <h2 className="font-bold text-sm tracking-wide">TOP ANALISTAS</h2>
            <div className="text-xs text-[var(--text-muted)] font-medium">Total de 1.247 usuários</div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-[0.65rem] font-bold uppercase text-[var(--text-muted)] tracking-widest bg-[var(--bg-secondary)]/50">
                  <th className="px-6 py-4">Rank</th>
                  <th className="px-6 py-4">Analista</th>
                  <th className="px-6 py-4">Accuracy</th>
                  <th className="px-6 py-4">Tier</th>
                  <th className="px-6 py-4 text-right">Pontos</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border-subtle)]">
                {rest.map((entry, i) => (
                  <tr key={entry.user_id} className="hover:bg-[var(--bg-secondary)]/30 transition-colors">
                    <td className="px-6 py-4">
                      <RankBadge rank={entry.rank} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-[var(--bg-secondary)] flex items-center justify-center font-bold text-sm">
                          {entry.display_name.charAt(0)}
                        </div>
                        <span className="font-semibold text-sm">{entry.display_name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 progress-bar">
                          <div 
                            className="progress-fill bg-[var(--accent-emerald)]"
                            style={{ width: `${entry.accuracy_rate * 100}%` }}
                          />
                        </div>
                        <span className="text-xs font-bold">{(entry.accuracy_rate * 100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-[0.6rem] font-bold uppercase px-2 py-1 bg-[var(--bg-secondary)] rounded-md">
                        {entry.tier}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="font-bold text-sm text-[var(--accent-emerald)]">
                        {entry.total_points.toLocaleString()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
