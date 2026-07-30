from fastapi import APIRouter, HTTPException
from app.services.database_service import get_citizen_profiles, get_citizen_history

router = APIRouter(prefix="/api/v1/welfare", tags=["citizens"])

@router.get("/citizens")
def list_citizens(limit: int = 50):
    """Retrieves a list of evaluated citizen profiles."""
    try:
        profiles = get_citizen_profiles(limit=limit)
        return {"status": "success", "count": len(profiles), "citizens": profiles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

@router.get("/citizens/{citizen_id}")
def get_citizen(citizen_id: int):
    """Retrieves complete historical recommendations, eligibility, and notifications for a citizen."""
    history = get_citizen_history(citizen_id)
    if not history:
        raise HTTPException(status_code=404, detail=f"Citizen ID #{citizen_id} not found.")
    return {"status": "success", "data": history}
