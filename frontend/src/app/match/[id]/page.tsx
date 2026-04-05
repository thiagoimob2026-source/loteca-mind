"use client";

import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import { api } from "@/lib/api";
import type { FusionResult, TicketSuggestion, MatchData } from "@/lib/types";

interface MatchPageProps {
  params: Promise<{ id: string }>;
}

function StatCard({ label, value, color, icon }: { label: string; value: string; color: string; icon: string }) {
  return (
    <div className="glass-card p-4 text-center">
      <div className="text-xl mb-1">{icon}</div>
      <div className="text-lg font-bold" style={{ color }}>
        {value}
      </div>
      <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
        {label}
      </div>
    </div>
  );
}

function FormBadge({ result }: { result: string }) {
  const styles: Record<string, { bg: string; color: string }> = {
    W: { bg: "rgba(16, 185, 129, 0.2)", color: "var(--accent-emerald)" },
    D: { bg: "rgba(245, 158, 11, 0.2)", color: "var(--accent-amber)" },
    L: { bg: "rgba(244, 63, 94, 0.2)", color: "var(--accent-rose)" },
  };
  const s = styles[result] || styles.D;
  return (
    <span
      className="w-7 h-7 rounded-md flex items-center justify-center text-xs font-bold"
      style={{ background: s.bg, color: s.color }}
    >
      {result}
    </span>
  );
}

export default function MatchDetailPage({ params }: MatchPageProps) {
  const { id } = use(params);
  const matchId = parseInt(id, 10);
  const router = useRouter();

  const [match, setMatch] = useState<MatchData | null>(null);
  const [fusion, setFusion] = useState<FusionResult | null>(null);
  const [suggestion, setSuggestion] = useState<TicketSuggestion | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.matches.get(matchId), api.predictions.get(matchId)])
      .then(([matchData, predData]) => {
        setMatch(matchData);
        setFusion(predData.fusion);
        setSuggestion(predData.suggestion);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [matchId]);

  if (loading) {
    return (
      <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
        <Navbar />
        <div className="flex items-center justify-center h-[60vh]">
          <div className="text-center">
            <div
              className="w-10 h-10 border-3 border-[var(--accent-emerald)] border-t-transparent rounded-full mx-auto mb-4"
              style={{ animation: "spin 0.8s linear infinite" }}
            />
            <p style={{ color: "var(--text-secondary)" }}>Carregando análise...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!match || !fusion) {
    return (
      <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
        <Navbar />
        <div className="flex items-center justify-center h-[60vh]">
          <p style={{ color: "var(--text-muted)" }}>Jogo não encontrado</p>
        </div>
      </div>
    );
  }

  const h = match.home_team;
  const a = match.away_team;

  return (
    <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
      <Navbar />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
        {/* Back Button */}
        <button
          onClick={() => router.push("/")}
          className="btn-secondary text-sm mb-6"
        >
          ← Voltar ao Hub
        </button>

        {/* Match Header */}
        <div
          className="glass-card p-8 mb-6 text-center"
          style={{ animation: "fade-in 0.5s ease-out" }}
        >
          <div className="text-xs mb-3" style={{ color: "var(--text-muted)", letterSpacing: "0.1em" }}>
            JOGO {fusion.match_id} • {match.competition}
          </div>
          <div className="flex items-center justify-center gap-6 mb-4">
            <div className="text-right flex-1">
              <div className="text-2xl font-bold" style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}>
                {h.name}
              </div>
              <div className="flex justify-end gap-1 mt-2">
                {h.form_last_5.map((r, i) => (
                  <FormBadge key={i} result={r} />
                ))}
              </div>
            </div>
            <div
              className="text-3xl font-bold px-5"
              style={{ color: "var(--accent-emerald)", fontFamily: "var(--font-outfit)" }}
            >
              VS
            </div>
            <div className="text-left flex-1">
              <div className="text-2xl font-bold" style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}>
                {a.name}
              </div>
              <div className="flex gap-1 mt-2">
                {a.form_last_5.map((r, i) => (
                  <FormBadge key={i} result={r} />
                ))}
              </div>
            </div>
          </div>
          <div className="text-xs" style={{ color: "var(--text-muted)" }}>
            📍 {match.venue}
          </div>
        </div>

        {/* Deep Analysis (Expert Verdict) */}
        {fusion.deep_analysis && (
          <div
            className="glass-card p-6 mb-6"
            style={{
              background: "linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(59, 130, 246, 0.05))",
              border: "1px solid rgba(16, 185, 129, 0.2)",
              animation: "slide-up 0.5s ease-out 0.05s backwards",
            }}
          >
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl">🎙️</span>
              <h3
                className="text-sm font-bold uppercase tracking-wider"
                style={{ color: "var(--accent-emerald)", fontFamily: "var(--font-outfit)" }}
              >
                Veredito do Analista
              </h3>
            </div>
            <p
              className="text-sm leading-relaxed font-medium italic"
              style={{ color: "var(--text-secondary)" }}
            >
              "{fusion.deep_analysis}"
            </p>
          </div>
        )}

        {/* Probability Cards */}
        <div className="grid grid-cols-3 gap-3 mb-6" style={{ animation: "slide-up 0.5s ease-out 0.1s backwards" }}>
          {[
            { label: "Vitória Mandante", prob: fusion.home_win_prob, icon: "🏠", col: "1" },
            { label: "Empate", prob: fusion.draw_prob, icon: "🤝", col: "X" },
            { label: "Vitória Visitante", prob: fusion.away_win_prob, icon: "✈️", col: "2" },
          ].map((item) => (
            <div
              key={item.col}
              className="glass-card p-5 text-center"
              style={{
                borderColor:
                  fusion.suggested_column === item.col
                    ? "rgba(16, 185, 129, 0.4)"
                    : "var(--border-subtle)",
                boxShadow:
                  fusion.suggested_column === item.col
                    ? "var(--shadow-glow-emerald)"
                    : "none",
              }}
            >
              <div className="text-2xl mb-2">{item.icon}</div>
              <div
                className="text-3xl font-bold"
                style={{
                  color:
                    fusion.suggested_column === item.col
                      ? "var(--accent-emerald)"
                      : "var(--text-secondary)",
                }}
              >
                {(item.prob * 100).toFixed(0)}%
              </div>
              <div className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
                Coluna {item.col} • {item.label}
              </div>
            </div>
          ))}
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6" style={{ animation: "slide-up 0.5s ease-out 0.2s backwards" }}>
          <StatCard label="xG Mandante" value={h.xg_accumulated.toFixed(2)} color="var(--accent-emerald)" icon="⚽" />
          <StatCard label="xG Visitante" value={a.xg_accumulated.toFixed(2)} color="var(--accent-cyan)" icon="⚽" />
          <StatCard label="Clutch Factor" value={`${(fusion.clutch_factor * 100).toFixed(0)}%`} color="var(--accent-violet)" icon="⚡" />
          <StatCard
            label="Clean Sheet %"
            value={`${(h.clean_sheet_rate * 100).toFixed(0)}% / ${(a.clean_sheet_rate * 100).toFixed(0)}%`}
            color="var(--accent-amber)"
            icon="🛡️"
          />
        </div>

        {/* Balance Bar */}
        <div className="glass-card p-6 mb-6" style={{ animation: "slide-up 0.5s ease-out 0.3s backwards" }}>
          <h3
            className="text-sm font-bold mb-4"
            style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}
          >
            ⚖️ Barra de Equilíbrio
          </h3>
          <div className="flex items-center gap-4">
            <div className="text-right flex-1">
              <div className="text-2xl font-bold" style={{ color: "var(--accent-blue)" }}>
                {fusion.reason_score.toFixed(0)}
              </div>
              <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
                RAZÃO
              </div>
            </div>
            <div
              className="flex-1 h-3 rounded-full overflow-hidden"
              style={{ background: "var(--bg-elevated)", maxWidth: "300px" }}
            >
              <div className="flex h-full">
                <div
                  className="h-full"
                  style={{ width: `${fusion.reason_score}%`, background: "var(--gradient-reason)" }}
                />
                <div
                  className="h-full"
                  style={{ width: `${fusion.emotion_score}%`, background: "var(--gradient-emotion)" }}
                />
              </div>
            </div>
            <div className="flex-1">
              <div className="text-2xl font-bold" style={{ color: "var(--accent-rose)" }}>
                {fusion.emotion_score.toFixed(0)}
              </div>
              <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
                EMOÇÃO
              </div>
            </div>
          </div>
        </div>

        {/* Insights */}
        {(fusion.key_factors.length > 0 || fusion.emotional_factors.length > 0) && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6" style={{ animation: "slide-up 0.5s ease-out 0.4s backwards" }}>
            {fusion.key_factors.length > 0 && (
              <div className="glass-card p-5">
                <h3 className="text-sm font-bold mb-3" style={{ color: "var(--accent-blue)" }}>
                  📊 Fatores Técnicos
                </h3>
                <ul className="space-y-2">
                  {fusion.key_factors.map((f, i) => (
                    <li
                      key={i}
                      className="text-xs pl-3"
                      style={{ color: "var(--text-secondary)", borderLeft: "2px solid var(--accent-blue)" }}
                    >
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {fusion.emotional_factors.length > 0 && (
              <div className="glass-card p-5">
                <h3 className="text-sm font-bold mb-3" style={{ color: "var(--accent-rose)" }}>
                  🧠 Fatores Emocionais
                </h3>
                <ul className="space-y-2">
                  {fusion.emotional_factors.map((f, i) => (
                    <li
                      key={i}
                      className="text-xs pl-3"
                      style={{ color: "var(--text-secondary)", borderLeft: "2px solid var(--accent-rose)" }}
                    >
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Zebra Alert */}
        {fusion.zebra_alert && fusion.zebra_insight && (
          <div
            className="glass-card p-6"
            style={{
              background: "linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(244, 63, 94, 0.08))",
              border: "1px solid rgba(139, 92, 246, 0.2)",
              animation: "slide-up 0.5s ease-out 0.5s backwards",
            }}
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">🦓</span>
              <h3 className="text-sm font-bold" style={{ color: "var(--accent-violet)" }}>
                Zebra Hunter Alert
              </h3>
            </div>
            <p className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
              {fusion.zebra_insight}
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
