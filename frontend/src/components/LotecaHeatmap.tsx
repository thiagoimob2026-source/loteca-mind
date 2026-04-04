"use client";

import { FusionResult, TicketSuggestion } from "@/lib/types";

interface HeatmapProps {
  fusions: FusionResult[];
  suggestions: TicketSuggestion[];
  ticketCost: number;
  totalCombinations: number;
}

function HeatmapCell({ fusion, suggestion }: { fusion: FusionResult; suggestion?: TicketSuggestion }) {
  const conf = fusion.overall_confidence;

  let bgColor: string;
  let borderColor: string;
  let textColor: string;

  if (conf >= 0.7) {
    bgColor = "rgba(16, 185, 129, 0.15)";
    borderColor = "rgba(16, 185, 129, 0.3)";
    textColor = "var(--accent-emerald)";
  } else if (conf >= 0.45) {
    bgColor = "rgba(245, 158, 11, 0.15)";
    borderColor = "rgba(245, 158, 11, 0.3)";
    textColor = "var(--accent-amber)";
  } else {
    bgColor = "rgba(244, 63, 94, 0.15)";
    borderColor = "rgba(244, 63, 94, 0.3)";
    textColor = "var(--accent-rose)";
  }

  return (
    <div
      className="relative rounded-xl p-3 transition-all duration-300 hover:scale-105 cursor-pointer"
      style={{ background: bgColor, border: `1px solid ${borderColor}` }}
      title={`${fusion.home_team} vs ${fusion.away_team} — Confiança: ${(conf * 100).toFixed(0)}%`}
    >
      <div className="text-center">
        <div className="text-[0.6rem] font-bold mb-1" style={{ color: "var(--text-muted)" }}>
          J{fusion.match_id}
        </div>
        <div className="text-lg font-bold" style={{ color: textColor }}>
          {fusion.suggested_column}
        </div>
        <div className="text-[0.6rem] font-semibold mt-1" style={{ color: textColor }}>
          {(conf * 100).toFixed(0)}%
        </div>
        {suggestion && suggestion.bet_type !== "simples" && (
          <div
            className="text-[0.55rem] mt-1 font-bold uppercase"
            style={{
              color: suggestion.bet_type === "duplo" ? "var(--accent-amber)" : "var(--accent-rose)",
            }}
          >
            {suggestion.bet_type}
          </div>
        )}
        {fusion.zebra_alert && (
          <div className="absolute -top-1 -right-1 text-sm">🦓</div>
        )}
      </div>
    </div>
  );
}

export default function LotecaHeatmap({ fusions, suggestions, ticketCost, totalCombinations }: HeatmapProps) {
  return (
    <div className="glass-card p-6" id="loteca-heatmap">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2
            className="text-lg font-bold"
            style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}
          >
            📊 Loteca Heatmap
          </h2>
          <p className="text-xs mt-1" style={{ color: "var(--text-secondary)" }}>
            Visão geral dos 14 jogos — trading dashboard
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold" style={{ color: "var(--accent-emerald)" }}>
            R$ {ticketCost.toFixed(2)}
          </div>
          <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
            {totalCombinations} combinações
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="flex gap-4 mb-4">
        {[
          { color: "var(--accent-emerald)", label: "Alta Confiança" },
          { color: "var(--accent-amber)", label: "Média — Duplo" },
          { color: "var(--accent-rose)", label: "Baixa — Zebra Zone" },
        ].map((item) => (
          <div key={item.label} className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: item.color }} />
            <span className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
              {item.label}
            </span>
          </div>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-7 gap-2">
        {fusions.map((fusion) => {
          const suggestion = suggestions.find((s) => s.match_id === fusion.match_id);
          return <HeatmapCell key={fusion.match_id} fusion={fusion} suggestion={suggestion} />;
        })}
      </div>

      {/* Summary Row */}
      <div
        className="grid grid-cols-3 gap-4 mt-5 pt-4"
        style={{ borderTop: "1px solid var(--border-subtle)" }}
      >
        <div className="text-center">
          <div className="text-xl font-bold" style={{ color: "var(--accent-emerald)" }}>
            {suggestions.filter((s) => s.bet_type === "simples").length}
          </div>
          <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
            Simples
          </div>
        </div>
        <div className="text-center">
          <div className="text-xl font-bold" style={{ color: "var(--accent-amber)" }}>
            {suggestions.filter((s) => s.bet_type === "duplo").length}
          </div>
          <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
            Duplos
          </div>
        </div>
        <div className="text-center">
          <div className="text-xl font-bold" style={{ color: "var(--accent-rose)" }}>
            {suggestions.filter((s) => s.bet_type === "triplo").length}
          </div>
          <div className="text-[0.65rem]" style={{ color: "var(--text-secondary)" }}>
            Triplos
          </div>
        </div>
      </div>
    </div>
  );
}
