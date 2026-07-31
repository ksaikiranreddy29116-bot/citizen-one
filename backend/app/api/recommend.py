from fastapi import APIRouter, HTTPException
from app.schemas.document import ExtractedDocumentSchema
from app.schemas.response import CitizenOneFinalResponse
from app.agents.orchestrator_agent import run_citizen_pipeline

router = APIRouter(prefix="/api/v1/welfare", tags=["welfare"])

@router.post("/recommend-schemes", response_model=CitizenOneFinalResponse)
async def recommend_schemes(citizen_data: ExtractedDocumentSchema):
    """
    Accepts pre-extracted citizen profile JSON and evaluates it through the workflow:
    eligibility validation -> scheme matching -> explanation -> notification.
    """
    try:
        response = await run_citizen_pipeline(citizen_data=citizen_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph execution failed: {str(e)}")
