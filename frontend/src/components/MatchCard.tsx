"use client";

import { FusionResult, TicketSuggestion } from "@/lib/types";

interface MatchCardProps {
  fusion: FusionResult;
  suggestion?: TicketSuggestion;
  index: number;
  onClick?: () => void;
}

function TemperatureIcon({ temp }: { temp: string }) {
  if (temp === "on_fire") return <span className="temp-on-fire text-xl">🔥</span>;
  if (temp === "cold") return <span className="temp-cold text-xl">❄️</span>;
  return <span className="temp-stable text-lg">⚡</span>;
}

function ConfidenceTag({ confidence }: { confidence: number }) {
  if (confidence >= 0.7) return <span className="tag tag-high">ALTA</span>;
  if (confidence >= 0.45) return <span className="tag tag-medium">MÉDIA</span>;
  return <span className="tag tag-low">BAIXA</span>;
}

function BetTypeTag({ type }: { type: string }) {
  const styles: Record<string, string> = {
    simples: "tag tag-high",
    duplo: "tag tag-medium",
    triplo: "tag tag-low",
  };
  return <span className={styles[type] || "tag"}>{type.toUpperCase()}</span>;
}

export default function MatchCard({ fusion, suggestion, index, onClick }: MatchCardProps) {
  const maxProb = Math.max(fusion.home_win_prob, fusion.draw_prob, fusion.away_win_prob);

  return (
    <div
      id={`match-card-${fusion.match_id}`}
      className="glass-card p-5 cursor-pointer group"
      style={{ animationDelay: `${index * 0.06}s`, animation: "slide-up 0.5s ease-out backwards" }}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span
            style={{
              color: "var(--text-muted)",
              fontSize: "0.75rem",
              fontWeight: 600,
              letterSpacing: "0.05em",
            }}
          >
            JOGO {fusion.match_id}
          </span>
          {fusion.zebra_alert && <span className="tag tag-zebra">🦓 ZEBRA</span>}
        </div>
        <div className="flex items-center gap-2">
          {suggestion && <BetTypeTag type={suggestion.bet_type} />}
          <ConfidenceTag confidence={fusion.overall_confidence} />
        </div>
      </div>

      {/* Teams */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2 flex-1">
          <TemperatureIcon temp={fusion.home_temperature} />
          <span className="font-semibold text-[var(--text-primary)] text-sm truncate">
            {fusion.home_team}
          </span>
        </div>
        <span
          style={{
            color: "var(--text-muted)",
            fontSize: "0.7rem",
            fontWeight: 700,
            letterSpacing: "0.1em",
            padding: "0 12px",
          }}
        >
          VS
        </span>
        <div className="flex items-center gap-2 flex-1 justify-end">
          <span className="font-semibold text-[var(--text-primary)] text-sm truncate text-right">
            {fusion.away_team}
          </span>
          <TemperatureIcon temp={fusion.away_temperature} />
        </div>
      </div>

      {/* Probability Bars */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        {[
          { label: "1", prob: fusion.home_win_prob, color: "var(--accent-emerald)" },
          { label: "X", prob: fusion.draw_prob, color: "var(--accent-amber)" },
          { label: "2", prob: fusion.away_win_prob, color: "var(--accent-cyan)" },
        ].map((item) => (
          <div key={item.label} className="text-center">
            <div
              className="text-xs font-bold mb-1"
              style={{
                color: item.prob === maxProb ? item.color : "var(--text-secondary)",
              }}
            >
              {item.label}
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${item.prob * 100}%`,
                  background:
                    item.prob === maxProb
                      ? item.color
                      : "var(--text-muted)",
                }}
              />
            </div>
            <div
              className="text-xs mt-1 font-semibold"
              style={{
                color: item.prob === maxProb ? item.color : "var(--text-muted)",
              }}
            >
              {(item.prob * 100).toFixed(0)}%
            </div>
          </div>
        ))}
      </div>

      {/* Balance Bar (Razão vs Emoção) */}
      <div className="mb-3">
        <div className="flex justify-between text-[0.65rem] font-semibold mb-1">
          <span style={{ color: "var(--accent-blue)" }}>
            RAZÃO {fusion.reason_score.toFixed(0)}%
          </span>
          <span style={{ color: "var(--accent-rose)" }}>
            {fusion.emotion_score.toFixed(0)}% EMOÇÃO
          </span>
        </div>
        <div className="flex h-[5px] rounded-full overflow-hidden" style={{ background: "var(--bg-elevated)" }}>
          <div
            className="h-full transition-all duration-700"
            style={{
              width: `${fusion.reason_score}%`,
              background: "var(--gradient-reason)",
            }}
          />
          <div
            className="h-full transition-all duration-700"
            style={{
              width: `${fusion.emotion_score}%`,
              background: "var(--gradient-emotion)",
            }}
          />
        </div>
      </div>

      {/* Suggested Column */}
      {suggestion && (
        <div
          className="flex items-center justify-between pt-3"
          style={{ borderTop: "1px solid var(--border-subtle)" }}
        >
          <span className="text-xs" style={{ color: "var(--text-secondary)" }}>
            Sugestão
          </span>
          <div className="flex gap-1">
            {suggestion.columns.map((col) => (
              <span
                key={col}
                className="px-3 py-1 rounded-md text-xs font-bold"
                style={{
                  background:
                    col === fusion.suggested_column
                      ? "rgba(16, 185, 129, 0.2)"
                      : "var(--bg-elevated)",
                  color:
                    col === fusion.suggested_column
                      ? "var(--accent-emerald)"
                      : "var(--text-secondary)",
                  border: `1px solid ${col === fusion.suggested_column ? "rgba(16, 185, 129, 0.3)" : "var(--border-subtle)"}`,
                }}
              >
                {col}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Clutch Factor (subtle) */}
      {fusion.clutch_factor > 0.6 && (
        <div className="mt-2 text-[0.65rem] text-right" style={{ color: "var(--accent-violet)" }}>
          ⚡ Clutch Factor: {(fusion.clutch_factor * 100).toFixed(0)}%
        </div>
      )}
    </div>
  );
}
