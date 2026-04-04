# Loteca Mind 🧠⚽

**Plataforma de previsão da Loteca Brasileira** combinando Ciência de Dados (xG, passes verticais) com Psicologia Esportiva (VAR stress, momentum, Lei do Ex).

> *Data-to-Dopamine Engine* — Transformamos estatística fria em experiência de jogo.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│              Frontend (Next.js)             │
│  The Hub • Match Detail • Leaderboard       │
└────────────────────┬────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────┐
│              Backend (FastAPI)              │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │ Ag. Alpha│ │ Ag. Psi  │ │ Ag. Strat. │  │
│  │ (Tático) │ │ (Psico.) │ │(Otimizador)│  │
│  └────┬─────┘ └────┬─────┘ └──────▲─────┘  │
│       └──────┬──────┘              │        │
│         Motor de Fusão ────────────┘        │
│         (Razão × Emoção)                    │
└─────────────────────────────────────────────┘
```

## 🤖 Os 3 Agentes de IA

| Agente | Função | Base Científica |
|--------|--------|-----------------|
| **Alpha** (Analista Tático) | xG, passes verticais, contra-ataques | Bai et al. (2021), Plakias (2024) |
| **Psi** (Psicólogo de Campo) | VAR stress, Lei do Ex, troca de técnico | Ivarsson (2019), Kaplánová (2024) |
| **Estrategista** (Otimizador) | Duplos/Triplos com budget de R$ 49,90 | Otimização combinatória |

## ⚡ Features

- 📊 **Loteca Heatmap** — Visão trading dashboard dos 14 jogos
- 🦓 **Zebra Hunter** — Onde a estatística diz uma coisa, mas o vestiário diz outra
- ⚖️ **Barra de Equilíbrio** — Razão (0-100) vs Emoção (0-100)
- 🔥❄️ **Indicador de Temperatura** — Time "on fire" ou em crise
- 🏆 **Global Leaderboard** — Ranking estilo Fantasy Premier League
- 🎖️ **Badges** — Mestre das Zebras, Estrategista Matemático, O Sensitivo

## 🚀 Quick Start

### Backend (Python/FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend (Next.js + Tailwind)
```bash
cd frontend
npm install
npm run dev
```

Acesse: **http://localhost:3000**

## 🗂️ Estrutura

```
LOTECA/
├── backend/
│   ├── app/
│   │   ├── agents/          # Alpha, Psi, Fusão, Estrategista
│   │   ├── models/          # Pydantic schemas
│   │   ├── routers/         # REST endpoints
│   │   ├── services/        # Data + Calibração
│   │   ├── prompts/         # System prompt (Gemini)
│   │   └── main.py          # FastAPI entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/             # Pages (Hub, Match, Leaderboard)
│   │   ├── components/      # MatchCard, Heatmap, ZebraHunter
│   │   └── lib/             # API client + Types
│   └── package.json
│
└── README.md
```

## 📋 Roadmap

- [x] **Fase 1** — MVP (3 agentes + frontend + mock data)
- [ ] **Fase 2A** — Supabase Auth (Google/Magic Link)
- [ ] **Fase 2B** — API de dados reais de futebol
- [ ] **Fase 2C** — Gemini insights textuais
- [ ] **Fase 3** — Gamificação completa + PWA + Calibração

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 16, Tailwind CSS 4, TypeScript |
| Backend | Python, FastAPI, Pydantic |
| IA | Google Gemini (Fase 2), Algoritmos proprietários |
| Auth | Supabase (Fase 2) |
| Database | Supabase PostgreSQL (Fase 2) |

## 📄 Licença

Projeto privado — Loteca Mind © 2026
