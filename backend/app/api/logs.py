from fastapi import APIRouter, HTTPException
from app.services.database_service import get_all_execution_logs

router = APIRouter(prefix="/api/v1/welfare", tags=["activity-logs"])

@router.get("/logs")
def get_logs(limit: int = 20):
    """Retrieves AI Activity Console execution trace logs."""
    try:
        logs = get_all_execution_logs(limit=limit)
        return {"status": "success", "count": len(logs), "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
