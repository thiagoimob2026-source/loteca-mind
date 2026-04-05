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
  const [isAdmin, setIsAdmin] = useState(false);
  
  // Admin Editor States
  const [showAdminEditor, setShowAdminEditor] = useState(false);
  const [adminRound, setAdminRound] = useState(1280);
  const [adminGrid, setAdminGrid] = useState<[string, string][]>(Array(14).fill(["", ""]));
  const [isSavingGrid, setIsSavingGrid] = useState(false);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadPrediction = async (retryCount = 0) => {
    setLoading(true);
    setError(null);
    try {
      // Tenta obter a última análise em cache antes de rodar uma nova
      const data = await api.predictions.latest();
      setPrediction(data);
      if (data && data.round_number) {
        setAdminRound(data.round_number);
      }
    } catch (err) {
      if (retryCount < 2) {
        // Render pode estar acordando — avisa e tenta de novo em 15s
        setError(`⏳ Servidor acordando... aguarde (tentativa ${retryCount + 1}/3)`);
        setTimeout(() => loadPrediction(retryCount + 1), 15000);
      } else {
        setError("Não foi possível conectar ao engine. Tente clicar em 'Recriar Análise' manualmente.");
        console.error(err);
        setLoading(false);
      }
    } finally {
      if (retryCount === 0 || retryCount >= 2) setLoading(false);
    }
  };

  const handleSaveGrid = async () => {
    setIsSavingGrid(true);
    try {
      await api.admin.updateConcurso(adminRound, adminGrid);
      alert("✅ Grade Loteca Mestre salva no Servidor!\n\nAgora você pode clicar em 'Recriar Nova Análise Completa' para disparar o motor RAG/AI e analisar estes novos times.");
      setShowAdminEditor(false);
    } catch (e: any) {
      alert("Erro ao salvar: " + e.message);
    } finally {
      setIsSavingGrid(false);
    }
  };

  useEffect(() => {
    // Verificação simples de painel Admin pela URL para ocultar botão dos usuários normais
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("admin") === "zebra14") {
      setIsAdmin(true);
      sessionStorage.setItem("loteca_admin_key", "active");
      // Limpa a URL para não deixar rastro (opcional)
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (sessionStorage.getItem("loteca_admin_key") === "active") {
      setIsAdmin(true);
    }

    // Carregamento base
    loadPrediction();
  }, []);

  const avgConfidence = prediction
    ? prediction.fusions.reduce((s, f) => s + f.overall_confidence, 0) / prediction.fusions.length
    : 0;

  const zebraCount = prediction ? prediction.fusions.filter((f) => f.zebra_alert).length : 0;

  return (
    <div className="min-h-screen theme-caixa" style={{ background: "var(--bg-primary)" }}>
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
            <span className="text-gradient">Rodada</span>{" "}
            <span style={{ color: "var(--text-primary)" }}>
               {prediction ? `Concurso da LOTECA #${prediction.round_number}` : "Painel Principal"}
            </span>
          </h1>
          <p className="text-base" style={{ color: "var(--text-secondary)" }}>
            A Força dos Dados Encontra o Clima do Vestiário
          </p>
          {prediction && (
            <p className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>
              {prediction.competition} • {prediction.fusions.length} jogos analisados
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

        {/* Generate Button (Admin Only) */}
        {isAdmin && (
          <div className="text-center mb-8" style={{ animation: "fade-in 0.3s ease-out" }}>
            <div className="inline-block bg-amber-500/10 text-amber-500 text-[10px] font-bold px-2 py-1 rounded mb-2 uppercase tracking-widest">
              Painel de Administração
            </div>
            <br />
            <button
              id="generate-analysis-btn"
              onClick={() => loadPrediction()}
              disabled={loading}
              className="btn-primary"
              style={{ opacity: loading ? 0.6 : 1, minWidth: "240px", background: "var(--accent-amber)", color: "#1a1a1a" }}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span
                    className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full"
                    style={{ animation: "spin 0.7s linear infinite" }}
                  />
                  Rodando RAG e IA...
                </span>
              ) : (
                "⚡ Recriar Nova Análise Completa"
              )}
            </button>
            <div className="mt-3">
              <button 
                onClick={() => {
                  setShowAdminEditor(!showAdminEditor);
                  setAdminGrid(Array(14).fill(["", ""])); // Reset limpo como pedido
                }}
                className="text-xs text-amber-500 font-bold underline cursor-pointer hover:text-amber-400"
              >
                {showAdminEditor ? "Fechar Editor de Grade" : "✏️ Editar Times do Próximo Concurso"}
              </button>
            </div>
            
            {/* Editor InLine */}
            {showAdminEditor && (
              <div className="mt-6 max-w-2xl mx-auto p-4 rounded-xl border-2 border-dashed border-amber-500/30" style={{ background: "var(--bg-card)", animation: "slide-up 0.3s ease" }}>
                <div className="mb-4 text-left">
                     <label className="text-xs font-bold text-gray-400 block mb-1">NÚMERO DO CONCURSO</label>
                     <input 
                       type="number" 
                       value={adminRound}
                       onChange={(e) => setAdminRound(parseInt(e.target.value) || 0)}
                       className="w-full bg-black/20 border border-gray-600 rounded p-2 text-white font-bold"
                     />
                </div>
                
                <div className="grid grid-cols-1 gap-2 mb-4">
                  {adminGrid.map((match, i) => (
                    <div key={i} className="flex gap-2 items-center bg-black/10 p-2 rounded">
                      <span className="text-amber-500 font-bold text-xs min-w-[20px]">{i+1}</span>
                      <input 
                        type="text" 
                        placeholder="Time Casa" 
                        value={match[0]}
                        onChange={(e) => {
                          const newGrid = [...adminGrid];
                          newGrid[i] = [e.target.value, newGrid[i][1]];
                          setAdminGrid(newGrid);
                        }}
                        className="w-1/2 bg-black/20 border border-gray-700 rounded p-1 text-sm text-center text-white outline-none focus:border-amber-500"
                      />
                      <span className="text-xs font-bold text-gray-500">x</span>
                      <input 
                        type="text" 
                        placeholder="Time Fora" 
                        value={match[1]}
                        onChange={(e) => {
                          const newGrid = [...adminGrid];
                          newGrid[i] = [newGrid[i][0], e.target.value];
                          setAdminGrid(newGrid);
                        }}
                        className="w-1/2 bg-black/20 border border-gray-700 rounded p-1 text-sm text-center text-white outline-none focus:border-amber-500"
                      />
                    </div>
                  ))}
                </div>
                
                <button
                  onClick={handleSaveGrid}
                  disabled={isSavingGrid}
                  className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-lg transition-colors"
                >
                  {isSavingGrid ? "Salvando..." : "💾 Salvar Concurso no Servidor"}
                </button>
              </div>
            )}
            
          </div>
        )}

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
