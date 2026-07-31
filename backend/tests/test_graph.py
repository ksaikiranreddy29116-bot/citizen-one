import pytest
from backend.app.schemas.document import ExtractedDocumentSchema
from backend.app.agents.orchestrator_agent import run_citizen_pipeline

@pytest.mark.asyncio
async def test_langgraph_pipeline_execution():
    profile = ExtractedDocumentSchema(
        full_name="Kavitha Reddy",
        dob="1985-06-20",
        income_annual=180000.0,
        state="Telangana",
        document_type="Income Certificate"
    )
    
    response = await run_citizen_pipeline(citizen_data=profile)
    
    assert response.extracted_data.full_name == "Kavitha Reddy"
    assert response.eligibility.eligible is True
    assert len(response.execution_logs) > 0
    assert len(response.explanation) > 0
    assert isinstance(response.documents_utilized, list)
