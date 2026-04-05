"use client";

import { FusionResult } from "@/lib/types";

interface ZebraHunterProps {
  fusions: FusionResult[];
}

export default function ZebraHunter({ fusions }: ZebraHunterProps) {
  const zebraMatches = fusions.filter((f) => f.zebra_alert);

  if (zebraMatches.length === 0) return null;

  return (
    <div className="glass-card p-6" id="zebra-hunter">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-3xl" style={{ animation: "float 2s ease-in-out infinite" }}>🦓</span>
        <div>
          <h3 className="text-lg font-bold" style={{ color: "var(--text-primary)", fontFamily: "var(--font-outfit)" }}>
            Caçador de Zebras
          </h3>
          <p className="text-xs" style={{ color: "var(--text-secondary)" }}>
            Onde a estatística diz uma coisa, mas o vestiário diz outra
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {zebraMatches.map((zm) => (
          <div
            key={zm.match_id}
            className="rounded-xl p-4 transition-all duration-300 hover:scale-[1.01]"
            style={{
              background: "linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(244, 63, 94, 0.08))",
              border: "1px solid rgba(139, 92, 246, 0.15)",
            }}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-sm" style={{ color: "var(--text-primary)" }}>
                {zm.home_team} vs {zm.away_team}
              </span>
              <span className="tag tag-zebra">JOGO {zm.match_id}</span>
            </div>
            {zm.zebra_insight && (
              <p className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                {zm.zebra_insight}
              </p>
            )}
            <div className="flex gap-3 mt-3">
              {zm.emotional_factors.slice(0, 2).map((factor, i) => (
                <span
                  key={i}
                  className="text-[0.65rem] px-2 py-1 rounded-lg"
                  style={{
                    background: "rgba(139, 92, 246, 0.1)",
                    color: "var(--accent-violet)",
                  }}
                >
                  {factor.substring(0, 60)}...
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
