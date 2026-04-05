"""
Loteca Mind — FastAPI Backend
Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import matches, predictions, leaderboard, admin, webhooks, auth

settings = get_settings()

app = FastAPI(
    title="Loteca Mind API",
    description="AI-powered Loteca prediction engine combining Data Science and Sports Psychology",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(matches.router)
app.include_router(predictions.router)
app.include_router(leaderboard.router)
app.include_router(admin.router)
app.include_router(webhooks.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    if settings.FOOTBALL_API_KEY:
        print("\n" + "="*50)
        print("🚀 LOTECA MIND BACKEND — LIVE MODE (API-Sports)")
        print(f"Gemini AI: {'ON' if settings.GEMINI_API_KEY else 'OFF (Mocking text)'}")
        print("="*50 + "\n")
    else:
        print("\n" + "!"*50)
        print("🚧 LOTECA MIND BACKEND — MOCK MODE (Simulated Data)")
        print("Configure FOOTBALL_API_KEY no .env para ativar dados reais.")
        print("!"*50 + "\n")


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online",
        "message": "Loteca Zebra 14 API — Data-to-Dopamine Engine 🧠⚽",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
