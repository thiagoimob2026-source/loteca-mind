"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";

export default function LoginPage() {
  const { user, loginWithGoogle, loginWithMagicLink } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [magicLinkSent, setMagicLinkSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [requiresPayment, setRequiresPayment] = useState(false);

  // If already logged in, redirect to home
  if (user) {
    router.push("/");
    return null;
  }

  const handleGoogleLogin = async () => {
    // Para simplificar a MVP, vamos desativar ou restringir Google Login se necessário.
    // Opcional Futuro: Checar VIP no Google Auth também!
    setLoading(true);
    setError(null);
    await loginWithGoogle();
    setLoading(false);
  };

  const handleMagicLink = async () => {
    if (!email.trim()) return;
    setLoading(true);
    setError(null);
    setRequiresPayment(false);

    try {
      // 1. Verificar se é VIP no Banco
      const { is_vip } = await api.auth.checkVip(email);
      
      if (!is_vip) {
        setRequiresPayment(true);
        setError("Este e-mail não possui uma assinatura Kiwify ativa.");
        setLoading(false);
        return;
      }

      // 2. Se for VIP, despacha o Magic Link real do Supabase
      const result = await loginWithMagicLink(email);
      if (result.success) {
        setMagicLinkSent(true);
      } else {
        setError(result.error || "Erro ao enviar link mágico");
      }
    } catch (err) {
      console.error(err);
      setError("Falha na comunicação com os servidores. Tente novamente.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row theme-caixa" style={{ background: "var(--bg-primary)" }}>
      {/* Leit Side - Premium Sales Pitch (Value Prop) */}
      <div 
        className="w-full md:w-5/12 p-8 md:p-12 flex flex-col justify-center relative overflow-hidden"
        style={{
          background: "linear-gradient(135deg, var(--accent-emerald-dim) 0%, var(--accent-cyan) 100%)",
          color: "white"
        }}
      >
        {/* Subtle background pattern */}
        <div className="absolute inset-0 opacity-10 bg-grid-pattern pointer-events-none" />

        <div className="relative z-10 max-w-md mx-auto">
          <Link href="/" className="inline-block mb-10 opacity-80 hover:opacity-100 transition-opacity">
            ← Voltar à Página Inicial
          </Link>

          <h2 className="text-3xl md:text-4xl font-bold mb-6 leading-tight" style={{ fontFamily: "var(--font-outfit)" }}>
            Desbloqueie os 14 Jogos da Rodada Atual.
          </h2>
          <p className="text-[1.05rem] opacity-90 mb-10 leading-relaxed">
            Seja um assinante VIP do <strong className="text-white">Loteca Zebra 14</strong> e tenha acesso irrestrito ao painel de inteligência artificial que os profissionais usam para fechar a grade.
          </p>

          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full flex items-center justify-center bg-white/20 text-white shrink-0 mt-1">🔓</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Acesso Ilimitado aos 14 Jogos</h3>
                <p className="text-sm opacity-80 leading-relaxed">Retire o cadeado e veja as probabilidades matemáticas e psicológicas completas de todos os jogos do concurso.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full flex items-center justify-center bg-white/20 text-white shrink-0 mt-1">🦓</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Caçador de Zebras</h3>
                <p className="text-sm opacity-80 leading-relaxed">Descubra as partidas onde a Zebra tem maior probabilidade de acontecer, com o Alerta Exclusivo de Zebra.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full flex items-center justify-center bg-white/20 text-white shrink-0 mt-1">📊</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Mapa de Calor da Loteca</h3>
                <p className="text-sm opacity-80 leading-relaxed">Acesse a proporção exata de onde investir em Duplos e Triplos para otimizar o custo do seu bilhete.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full flex items-center justify-center bg-white/20 text-white shrink-0 mt-1">🔬</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Psicologia Científica (RAG AI)</h3>
                <p className="text-sm border-l-2 border-emerald-400 pl-3 opacity-90 leading-relaxed font-medium">O único painel do Brasil que calibra o Fator Emocional em tempo real usando Literatura Científica (Li & Pan, Jekauc et al.) ao varrer as notícias do time.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full md:w-7/12 flex items-center justify-center p-6 md:p-12 relative">
        <div className="glass-card p-8 md:p-10 w-full max-w-md shadow-xl border-t-4" style={{ borderColor: "var(--accent-rose)", animation: "slide-up 0.5s ease-out" }}>
          {/* Logo */}
          <div className="text-center mb-8">
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center text-2xl font-bold mx-auto mb-4"
              style={{
                background: "linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan))",
                color: "white",
              }}
            >
              L
            </div>
            <h1
              className="text-2xl font-bold"
              style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}
            >
              Loteca <span className="text-gradient">Zebra 14</span>
            </h1>
            <p className="text-sm mt-2" style={{ color: "var(--text-secondary)" }}>
              Acesso exclusivo para assinantes VIP
            </p>
          </div>

          {magicLinkSent ? (
            /* Magic Link Sent Message */
            <div className="text-center py-6 animate-fade-in">
              <div className="text-5xl mb-4">📩</div>
              <h2 className="text-xl font-bold mb-2" style={{ color: "var(--text-primary)" }}>
                Link enviado ao seu E-mail!
              </h2>
              <p className="text-sm mb-6 leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                Cheque a caixa de entrada para <strong>{email}</strong>. Clique no botão de acesso que acabamos de mandar.
              </p>
              <button
                onClick={() => setMagicLinkSent(false)}
                className="btn-secondary w-full text-sm font-bold"
              >
                Voltar e tentar outro e-mail
              </button>
            </div>
          ) : (
            <>
              {/* Google Login */}
              <button
                onClick={handleGoogleLogin}
                disabled={loading}
                className="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-xl font-bold text-sm transition-all duration-300 transform hover:-translate-y-1"
                style={{
                  background: "var(--bg-card)",
                  border: "1px solid var(--accent-emerald)",
                  color: "var(--text-primary)",
                  boxShadow: "var(--shadow-card)",
                }}
              >
                <svg width="20" height="20" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.56c2.08-1.92 3.28-4.74 3.28-8.1z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.56-2.77c-.98.66-2.23 1.06-3.72 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                </svg>
                Continuar com Google (Rápido)
              </button>

              {/* Divider */}
              <div className="flex items-center gap-3 my-6">
                <div className="flex-1 h-px" style={{ background: "var(--border-subtle)" }} />
                <span className="text-xs font-bold uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>Ou Faça Login Por Email</span>
                <div className="flex-1 h-px" style={{ background: "var(--border-subtle)" }} />
              </div>

              {/* Magic Link */}
              <div>
                <label className="text-xs font-bold mb-2 block" style={{ color: "var(--text-secondary)" }}>
                  Email de Assinante (Link Mágico)
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="seu@email.com"
                  className="w-full px-4 py-3 rounded-xl text-sm font-medium outline-none transition-all duration-200"
                  style={{
                    background: "var(--bg-secondary)",
                    border: "1px solid var(--border-subtle)",
                    color: "var(--text-primary)",
                  }}
                  onFocus={(e) => (e.target.style.borderColor = "var(--accent-rose)")}
                  onBlur={(e) => (e.target.style.borderColor = "var(--border-subtle)")}
                  onKeyDown={(e) => e.key === "Enter" && handleMagicLink()}
                />
                <button
                  onClick={handleMagicLink}
                  disabled={loading || !email.trim()}
                  className="w-full mt-4 py-3 rounded-xl text-white font-bold transition-all duration-300 shadow-lg"
                  style={{ 
                    background: "var(--accent-rose)",
                    opacity: loading || !email.trim() ? 0.5 : 1,
                    transform: (loading || !email.trim()) ? "none" : "translateY(-2px)"
                  }}
                >
                  {loading ? "Enviando Autenticação..." : "Receber Acesso no E-mail 🚀"}
                </button>
              </div>

              {/* Error */}
              {error && (
                <div className="p-3 rounded-lg mt-4 text-xs font-bold text-center border" style={{ backgroundColor: "rgba(218, 41, 28, 0.1)", color: "var(--accent-rose)", border: "1px solid rgba(218, 41, 28, 0.2)" }}>
                  {error}
                </div>
              )}

              {/* Kiwify Checkout Redirect (Shown if email not VIP) */}
              {requiresPayment && (
                <div className="mt-6 text-center animate-fade-in flex flex-col gap-3">
                  <a
                    href="https://pay.kiwify.com.br/OyaEgln"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-white font-bold transition-all duration-300 shadow-xl"
                    style={{ background: "linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan))" }}
                  >
                    🛒 Assinar Plano Mensal (Acesso VIP)
                  </a>
                  <a
                    href="https://pay.kiwify.com.br/5Tj04gy"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-white font-bold transition-all duration-300 shadow-md border"
                    style={{ background: "transparent", borderColor: "var(--accent-emerald)", color: "var(--accent-emerald)" }}
                  >
                    🚀 Melhor Custo-Benefício: Plano Anual
                  </a>
                  <p className="text-[0.65rem] text-center mt-2 opacity-70" style={{ color: "var(--text-secondary)" }}>
                    Você será redirecionado para a página segura da Kiwify. O cadastro será ativado instantaneamente.
                  </p>
                </div>
              )}
            </>
          )}

          {/* Footer */}
          <p className="text-[0.65rem] text-center mt-8 font-medium" style={{ color: "var(--text-muted)" }}>
            Ao assinar e entrar, você concorda firmemente com nossos Termos de Serviço e a Política de Isenção de Risco Analítico.
          </p>
        </div>
      </div>
    </div>
  );
}
