"""
AI LMS – Quiz Performance Analysis API
Entry point: FastAPI app with all routes mounted.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import quiz, health
from config.settings import settings

app = FastAPI(
    title="AI LMS – Quiz Performance Analyzer",
    description="AI-powered student quiz analysis: scoring, weak topic detection, grade & personalized feedback.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(quiz.router,   prefix="/api/quiz", tags=["Quiz Analysis"])


@app.get("/", tags=["Root"])
def root():
    return {
        "service": "AI LMS Quiz Performance Analyzer",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
