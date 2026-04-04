"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/", label: "The Hub", icon: "🏠" },
  { href: "/leaderboard", label: "Ranking", icon: "🏆" },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav
      className="sticky top-0 z-50"
      style={{
        background: "rgba(255, 255, 255, 0.85)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        borderBottom: "1px solid var(--border-subtle)",
      }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center text-lg font-bold"
              style={{
                background: "linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan))",
                color: "white",
              }}
            >
              L
            </div>
            <div>
              <span
                className="font-bold text-base"
                style={{ fontFamily: "var(--font-outfit)", color: "var(--text-primary)" }}
              >
                Loteca{" "}
                <span className="text-gradient">Mind</span>
              </span>
              <div className="text-[0.55rem] -mt-0.5" style={{ color: "var(--text-muted)" }}>
                Data-to-Dopamine
              </div>
            </div>
          </Link>

          {/* Navigation */}
          <div className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                  style={{
                    background: isActive ? "rgba(5, 150, 105, 0.08)" : "transparent",
                    color: isActive ? "var(--accent-emerald)" : "var(--text-secondary)",
                    border: isActive ? "1px solid rgba(5, 150, 105, 0.15)" : "1px solid transparent",
                  }}
                >
                  <span>{item.icon}</span>
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Status */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div
                className="w-2 h-2 rounded-full"
                style={{
                  background: "var(--accent-emerald)",
                  animation: "pulse-slow 2s ease-in-out infinite",
                }}
              />
              <span className="text-xs" style={{ color: "var(--text-secondary)" }}>
                Engine Online
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
