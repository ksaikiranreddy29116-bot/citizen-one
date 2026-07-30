from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.recommend import router as recommend_router
from app.api.citizens import router as citizens_router
from app.api.logs import router as logs_router
from app.api.notifications import router as notifications_router
from app.api.health import router as health_router

app = FastAPI(
    title="CitizenOne Welfare Platform API",
    description="Production AI-Powered Government Welfare Recommendation Platform using LangGraph Multi-Agent Architecture",
    version="1.0.0"
)

# Enable CORS for React Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(upload_router)
app.include_router(recommend_router)
app.include_router(citizens_router)
app.include_router(logs_router)
app.include_router(notifications_router)
app.include_router(health_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "CitizenOne - LangGraph Multi-Agent Orchestrator Platform"
    }