from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas.response import CitizenOneFinalResponse
from app.agents.orchestrator_agent import run_citizen_pipeline

router = APIRouter(prefix="/api/v1/welfare", tags=["welfare"])

@router.post("/extract-document", response_model=CitizenOneFinalResponse)
async def extract_document(file: UploadFile = File(...)):
    """
    Uploads a government ID image to run the entire multi-agent LangGraph workflow:
    OCR extraction -> eligibility validation -> scheme matching -> explanation -> notification.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image format (JPEG/PNG).")
    
    try:
        image_bytes = await file.read()
        response = await run_citizen_pipeline(document_bytes=image_bytes)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph execution failed: {str(e)}")
