"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const { user, loginWithGoogle, loginWithMagicLink } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [magicLinkSent, setMagicLinkSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // If already logged in, redirect to home
  if (user) {
    router.push("/");
    return null;
  }

  const handleGoogleLogin = async () => {
    setLoading(true);
    setError(null);
    await loginWithGoogle();
    setLoading(false);
  };

  const handleMagicLink = async () => {
    if (!email.trim()) return;
    setLoading(true);
    setError(null);
    const result = await loginWithMagicLink(email);
    if (result.success) {
      setMagicLinkSent(true);
    } else {
      setError(result.error || "Erro ao enviar link");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "var(--bg-primary)" }}>
      <div className="glass-card p-8 w-full max-w-md" style={{ animation: "slide-up 0.5s ease-out" }}>
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
            Loteca <span className="text-gradient">Mind</span>
          </h1>
          <p className="text-sm mt-2" style={{ color: "var(--text-secondary)" }}>
            Entre para acessar suas previsões e ranking
          </p>
        </div>

        {magicLinkSent ? (
          /* Magic Link Sent Message */
          <div className="text-center py-6">
            <div className="text-4xl mb-3">📩</div>
            <h2 className="text-lg font-semibold mb-2" style={{ color: "var(--text-primary)" }}>
              Link enviado!
            </h2>
            <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
              Verifique seu email <strong>{email}</strong> e clique no link para entrar.
            </p>
            <button
              onClick={() => setMagicLinkSent(false)}
              className="btn-secondary mt-4 text-sm"
            >
              Tentar outro email
            </button>
          </div>
        ) : (
          <>
            {/* Google Login */}
            <button
              onClick={handleGoogleLogin}
              disabled={loading}
              className="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-xl font-medium text-sm transition-all duration-200"
              style={{
                background: "var(--bg-card)",
                border: "1px solid var(--border-light)",
                color: "var(--text-primary)",
                boxShadow: "var(--shadow-card)",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.boxShadow = "var(--shadow-card-hover)")}
              onMouseLeave={(e) => (e.currentTarget.style.boxShadow = "var(--shadow-card)")}
            >
              <svg width="20" height="20" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.56c2.08-1.92 3.28-4.74 3.28-8.1z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.56-2.77c-.98.66-2.23 1.06-3.72 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
              </svg>
              Entrar com Google
            </button>

            {/* Divider */}
            <div className="flex items-center gap-3 my-6">
              <div className="flex-1 h-px" style={{ background: "var(--border-subtle)" }} />
              <span className="text-xs" style={{ color: "var(--text-muted)" }}>ou</span>
              <div className="flex-1 h-px" style={{ background: "var(--border-subtle)" }} />
            </div>

            {/* Magic Link */}
            <div>
              <label className="text-xs font-medium mb-2 block" style={{ color: "var(--text-secondary)" }}>
                Email (Magic Link)
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                className="w-full px-4 py-3 rounded-xl text-sm outline-none transition-all duration-200"
                style={{
                  background: "var(--bg-secondary)",
                  border: "1px solid var(--border-subtle)",
                  color: "var(--text-primary)",
                }}
                onFocus={(e) => (e.target.style.borderColor = "var(--accent-emerald)")}
                onBlur={(e) => (e.target.style.borderColor = "var(--border-subtle)")}
                onKeyDown={(e) => e.key === "Enter" && handleMagicLink()}
              />
              <button
                onClick={handleMagicLink}
                disabled={loading || !email.trim()}
                className="btn-primary w-full mt-3"
                style={{ opacity: loading || !email.trim() ? 0.5 : 1 }}
              >
                {loading ? "Enviando..." : "Enviar Link Mágico ✨"}
              </button>
            </div>

            {/* Error */}
            {error && (
              <p className="text-xs text-center mt-4" style={{ color: "var(--accent-rose)" }}>
                {error}
              </p>
            )}
          </>
        )}

        {/* Footer */}
        <p className="text-[0.6rem] text-center mt-6" style={{ color: "var(--text-muted)" }}>
          Ao continuar, você concorda com os Termos de Serviço
        </p>
      </div>
    </div>
  );
}
