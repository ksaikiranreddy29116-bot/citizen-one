from typing import Optional
from app.schemas.document import ExtractedDocumentSchema
from app.schemas.response import CitizenOneFinalResponse
from app.graph.citizen_graph import citizen_graph
from app.services.database_service import save_full_pipeline_run

async def run_citizen_pipeline(
    document_bytes: Optional[bytes] = None,
    citizen_data: Optional[ExtractedDocumentSchema] = None
) -> CitizenOneFinalResponse:
    """
    Coordinates execution of the multi-agent workflow via LangGraph,
    returning the consolidated Response object and logging the run.
    """
    # Build initial LangGraph workflow state
    initial_state = {
        "document_bytes": document_bytes,
        "input_citizen_data": citizen_data,
        "extracted_data": None,
        "eligibility": None,
        "recommendations": None,
        "explanation": "",
        "notifications": [],
        "execution_logs": [],
        "matching_criteria": [],
        "missing_requirements": [],
        "documents_utilized": []
    }
    
    # Run the orchestrated graph asynchronously
    final_state = await citizen_graph.ainvoke(initial_state)
    
    # Compile response model
    response = CitizenOneFinalResponse(
        extracted_data=final_state["extracted_data"],
        eligibility=final_state["eligibility"],
        recommendations=final_state["recommendations"],
        explanation=final_state["explanation"],
        notifications=final_state["notifications"],
        execution_logs=final_state["execution_logs"],
        matching_criteria=final_state["matching_criteria"],
        missing_requirements=final_state["missing_requirements"],
        documents_utilized=final_state["documents_utilized"]
    )
    
    # Persist full multi-agent pipeline evaluation run to relational database
    try:
        citizen_id = save_full_pipeline_run(response)
        response.execution_logs.append(f"[Database Service] Persisted evaluation run under Citizen ID: #{citizen_id}")
    except Exception as db_err:
        print(f"⚠️ Audit logging error: {db_err}")
        
    return response
