import type { Metadata, Viewport } from "next";
import { Inter, Outfit } from "next/font/google";
import Providers from "./providers";
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
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="apple-touch-icon" href="/icons/icon-192.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
      </head>
      <body className="min-h-screen bg-grid-pattern" style={{ fontFamily: "var(--font-inter)" }}>
        <Providers>{children}</Providers>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                  navigator.serviceWorker.register('/sw.js');
                });
              }
            `,
          }}
        />
      </body>
    </html>
  );
}
