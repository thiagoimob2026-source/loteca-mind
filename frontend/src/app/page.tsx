"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import MatchCard from "@/components/MatchCard";
import LotecaHeatmap from "@/components/LotecaHeatmap";
import ZebraHunter from "@/components/ZebraHunter";
import { api } from "@/lib/api";
import type { LotecaPrediction } from "@/lib/types";

export default function HomePage() {
  const router = useRouter();
  const [prediction, setPrediction] = useState<LotecaPrediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadPrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.predictions.analyze();
      setPrediction(data);
    } catch (err) {
      setError("Não foi possível conectar ao engine. Verifique se o backend está rodando.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPrediction();
  }, []);

  const avgConfidence = prediction
    ? prediction.fusions.reduce((s, f) => s + f.overall_confidence, 0) / prediction.fusions.length
    : 0;

  const zebraCount = prediction ? prediction.fusions.filter((f) => f.zebra_alert).length : 0;

  return (
    <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {/* Hero Section */}
        <div
          className="text-center mb-10"
          style={{ animation: "fade-in 0.6s ease-out" }}
        >
          <h1
            className="text-4xl sm:text-5xl font-bold mb-3"
            style={{ fontFamily: "var(--font-outfit)" }}
          >
            <span className="text-gradient">Matchday</span>{" "}
            <span style={{ color: "var(--text-primary)" }}>Analysis</span>
          </h1>
          <p className="text-base" style={{ color: "var(--text-secondary)" }}>
            Razão × Emoção — Data Science meets Sports Psychology
          </p>
          {prediction && (
            <p className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>
              Rodada {prediction.round_number} • {prediction.competition} • {prediction.fusions.length} jogos analisados
            </p>
          )}
        </div>

        {/* Stats Summary */}
        {prediction && (
          <div
            className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8"
            style={{ animation: "slide-up 0.5s ease-out 0.1s backwards" }}
          >
            {[
              {
                label: "Ticket Estimado",
                value: `R$ ${prediction.strategy.ticket_cost.toFixed(2)}`,
                color: "var(--accent-emerald)",
                icon: "💰",
              },
              {
                label: "Confiança Média",
                value: `${(avgConfidence * 100).toFixed(0)}%`,
                color: "var(--accent-cyan)",
                icon: "📊",
              },
              {
                label: "Alertas Zebra",
                value: zebraCount.toString(),
                color: "var(--accent-violet)",
                icon: "🦓",
              },
              {
                label: "Combinações",
                value: prediction.strategy.total_combinations.toLocaleString(),
                color: "var(--accent-amber)",
                icon: "🎯",
              },
            ].map((stat) => (
              <div key={stat.label} className="glass-card p-4 text-center">
                <div className="text-2xl mb-1">{stat.icon}</div>
                <div className="text-xl font-bold" style={{ color: stat.color }}>
                  {stat.value}
                </div>
                <div className="text-[0.65rem] mt-1" style={{ color: "var(--text-secondary)" }}>
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Generate Button */}
        <div className="text-center mb-8">
          <button
            id="generate-analysis-btn"
            onClick={loadPrediction}
            disabled={loading}
            className="btn-primary"
            style={{ opacity: loading ? 0.6 : 1, minWidth: "240px" }}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span
                  className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full"
                  style={{ animation: "spin 0.7s linear infinite" }}
                />
                Analisando...
              </span>
            ) : (
              "⚡ Gerar Nova Análise"
            )}
          </button>
        </div>

        {/* Error State */}
        {error && (
          <div
            className="glass-card p-6 text-center mb-8"
            style={{ borderColor: "rgba(244, 63, 94, 0.3)" }}
          >
            <div className="text-3xl mb-3">⚠️</div>
            <p className="text-sm" style={{ color: "var(--accent-rose)" }}>
              {error}
            </p>
            <p className="text-xs mt-2" style={{ color: "var(--text-muted)" }}>
              Execute: <code className="px-2 py-1 rounded" style={{ background: "var(--bg-elevated)" }}>
                cd backend && uvicorn app.main:app --reload
              </code>
            </p>
          </div>
        )}

        {/* Main Content */}
        {prediction && (
          <>
            {/* Heatmap */}
            <div className="mb-8" style={{ animation: "slide-up 0.5s ease-out 0.2s backwards" }}>
              <LotecaHeatmap
                fusions={prediction.fusions}
                suggestions={prediction.strategy.suggestions}
                ticketCost={prediction.strategy.ticket_cost}
                totalCombinations={prediction.strategy.total_combinations}
              />
            </div>

            {/* Match Cards Grid */}
            <div className="mb-8">
              <h2
                className="text-xl font-bold mb-5"
                style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}
              >
                🏟️ Análise Detalhada dos 14 Jogos
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {prediction.fusions.map((fusion, index) => {
                  const suggestion = prediction.strategy.suggestions.find(
                    (s) => s.match_id === fusion.match_id
                  );
                  return (
                    <MatchCard
                      key={fusion.match_id}
                      fusion={fusion}
                      suggestion={suggestion}
                      index={index}
                      onClick={() => router.push(`/match/${fusion.match_id}`)}
                    />
                  );
                })}
              </div>
            </div>

            {/* Zebra Hunter */}
            <div style={{ animation: "slide-up 0.5s ease-out 0.4s backwards" }}>
              <ZebraHunter fusions={prediction.fusions} />
            </div>

            {/* Footer Info */}
            <div className="text-center mt-12 mb-4">
              <p className="text-xs" style={{ color: "var(--text-muted)" }}>
                Análise gerada em {new Date(prediction.generated_at).toLocaleString("pt-BR")}
              </p>
              <p className="text-[0.6rem] mt-1" style={{ color: "var(--text-muted)" }}>
                Powered by Agente Alpha (Tático) × Agente Psi (Psicológico) × Motor de Fusão
              </p>
            </div>
          </>
        )}

        {/* Loading skeleton */}
        {loading && !prediction && (
          <div className="space-y-4">
            {[...Array(6)].map((_, i) => (
              <div
                key={i}
                className="glass-card p-6 h-48"
                style={{
                  animation: `shimmer 2s linear infinite`,
                  background: `linear-gradient(90deg, var(--bg-card) 0%, var(--bg-card-hover) 50%, var(--bg-card) 100%)`,
                  backgroundSize: "200% 100%",
                }}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
