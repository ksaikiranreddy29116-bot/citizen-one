from fastapi import APIRouter, HTTPException
from app.services.database_service import get_all_notifications

router = APIRouter(prefix="/api/v1/welfare", tags=["notifications"])

@router.get("/notifications")
def list_notifications(limit: int = 50):
    """Retrieves generated calendar notifications and document alerts."""
    try:
        notifications = get_all_notifications(limit=limit)
        return {"status": "success", "count": len(notifications), "notifications": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
