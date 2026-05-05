"""
Health check route.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health", summary="Health check")
def health_check():
    return {
        "status": "ok",
        "service": "AI LMS Quiz Performance Analyzer",
        "timestamp": datetime.utcnow().isoformat(),
    }
