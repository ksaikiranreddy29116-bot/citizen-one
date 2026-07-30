from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, START, END
from app.schemas.document import ExtractedDocumentSchema
from app.schemas.eligibility import EligibilitySchema
from app.schemas.recommendation import RecommendationResponseSchema
from app.schemas.response import NotificationSchema

from app.agents.document_agent import run_document_autofill_agent
from app.agents.eligibility_agent import run_eligibility_agent
from app.agents.recommendation_agent import run_scheme_recommendation_agent
from app.agents.explanation_agent import run_explanation_agent
from app.agents.notification_agent import run_notification_agent

class CitizenGraphState(TypedDict):
    # Inputs
    document_bytes: Optional[bytes]
    input_citizen_data: Optional[ExtractedDocumentSchema]
    
    # State tracking & outputs
    extracted_data: Optional[ExtractedDocumentSchema]
    eligibility: Optional[EligibilitySchema]
    recommendations: Optional[RecommendationResponseSchema]
    explanation: Optional[str]
    notifications: Optional[List[NotificationSchema]]
    
    # Tracing & Activity Logs
    execution_logs: List[str]
    matching_criteria: List[str]
    missing_requirements: List[str]
    documents_utilized: List[str]

async def document_agent_node(state: CitizenGraphState) -> Dict[str, Any]:
    logs = list(state.get("execution_logs", []))
    docs = list(state.get("documents_utilized", []))
    
    logs.append("[Document Agent] processing source document.")
    
    if state.get("document_bytes"):
        extracted = await run_document_autofill_agent(state["document_bytes"])
        docs.append(extracted.document_type)
        logs.append(f"[Document Agent] document type detected: {extracted.document_type}")
    elif state.get("input_citizen_data"):
        extracted = state["input_citizen_data"]
        docs.append(extracted.document_type)
        logs.append("[Document Agent] bypassed OCR; running pipeline using input profile JSON.")
    else:
        extracted = ExtractedDocumentSchema(document_type="None/Missing")
        logs.append("[Document Agent] no document provided.")
        
    return {
        "extracted_data": extracted,
        "execution_logs": logs,
        "documents_utilized": docs
    }

async def eligibility_agent_node(state: CitizenGraphState) -> Dict[str, Any]:
    logs = list(state.get("execution_logs", []))
    criteria = list(state.get("matching_criteria", []))
    missing = list(state.get("missing_requirements", []))
    
    logs.append("[Eligibility Agent] verifying government rules.")
    extracted = state.get("extracted_data")
    
    eligibility = await run_eligibility_agent(extracted)
    
    # Map verification rules to trace metrics
    for rule in eligibility.rule_validations:
        logs.append(f"   - Rule '{rule.rule_name}': {'PASSED' if rule.passed else 'FAILED'} ({rule.reason})")
        if rule.passed:
            criteria.append(rule.rule_name)
        else:
            missing.append(rule.rule_name)
            
    logs.append(f"[Eligibility Agent] result: {eligibility.validation_reason}")
    return {
        "eligibility": eligibility,
        "execution_logs": logs,
        "matching_criteria": criteria,
        "missing_requirements": missing
    }

async def recommendation_agent_node(state: CitizenGraphState) -> Dict[str, Any]:
    logs = list(state.get("execution_logs", []))
    logs.append("[Recommendation Agent] evaluating welfare schemes.")
    extracted = state.get("extracted_data")
    
    recs = await run_scheme_recommendation_agent(extracted)
    logs.append(f"[Recommendation Agent] matching complete. Recommended {len(recs.recommended_schemes)} welfare program(s).")
    
    return {
        "recommendations": recs,
        "execution_logs": logs
    }

async def explanation_agent_node(state: CitizenGraphState) -> Dict[str, Any]:
    logs = list(state.get("execution_logs", []))
    logs.append("[Explanation Agent] creating friendly conversational summary.")
    
    extracted = state.get("extracted_data")
    eligibility = state.get("eligibility")
    recs = state.get("recommendations")
    
    explanation = await run_explanation_agent(extracted, eligibility, recs)
    logs.append("[Explanation Agent] conversational summary generated.")
    
    return {
        "explanation": explanation,
        "execution_logs": logs
    }

async def notification_agent_node(state: CitizenGraphState) -> Dict[str, Any]:
    logs = list(state.get("execution_logs", []))
    logs.append("[Notification Agent] identifying reminders and alerts.")
    
    extracted = state.get("extracted_data")
    recs = state.get("recommendations")
    
    notifs = await run_notification_agent(extracted, recs)
    logs.append(f"[Notification Agent] generated {len(notifs)} notification(s).")
    
    return {
        "notifications": notifs,
        "execution_logs": logs
    }

# Build and compile StateGraph
workflow = StateGraph(CitizenGraphState)
workflow.add_node("document_agent", document_agent_node)
workflow.add_node("eligibility_agent", eligibility_agent_node)
workflow.add_node("recommendation_agent", recommendation_agent_node)
workflow.add_node("explanation_agent", explanation_agent_node)
workflow.add_node("notification_agent", notification_agent_node)

workflow.add_edge(START, "document_agent")
workflow.add_edge("document_agent", "eligibility_agent")
workflow.add_edge("eligibility_agent", "recommendation_agent")
workflow.add_edge("recommendation_agent", "explanation_agent")
workflow.add_edge("explanation_agent", "notification_agent")
workflow.add_edge("notification_agent", END)

citizen_graph = workflow.compile()
