"""
Loteca Mind — FastAPI Backend
Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import matches, predictions, leaderboard

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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(matches.router)
app.include_router(predictions.router)
app.include_router(leaderboard.router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online",
        "message": "Loteca Mind API — Data-to-Dopamine Engine 🧠⚽",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
