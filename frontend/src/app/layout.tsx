import type { Metadata, Viewport } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Loteca Mind — IA + Psicologia Esportiva",
  description:
    "Plataforma de previsão da Loteca Brasileira combinando Ciência de Dados e Psicologia Esportiva. Análise dos 14 jogos com inteligência artificial.",
  keywords: ["loteca", "previsão", "futebol", "xG", "psicologia esportiva", "IA"],
  authors: [{ name: "Loteca Mind" }],
};

export const viewport: Viewport = {
  themeColor: "#f8f9fc",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${outfit.variable}`}>
      <body className="min-h-screen bg-grid-pattern" style={{ fontFamily: "var(--font-inter)" }}>
        {children}
      </body>
    </html>
  );
}
