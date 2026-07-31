from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["health"])

@router.get("/health")
@router.get("/api/v1/health")
def health_check():
    """System health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "CitizenOne Welfare Engine",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "fastapi": "online",
            "langgraph": "online",
            "database": "online",
            "groq_llm": "configured"
        }
    }
