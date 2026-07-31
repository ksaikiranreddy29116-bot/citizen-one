from pydantic import BaseModel, Field
from typing import List, Optional
from .document import ExtractedDocumentSchema
from .eligibility import EligibilitySchema
from .recommendation import RecommendationResponseSchema

class NotificationSchema(BaseModel):
    """Schema for individual citizen alerts and reminders."""
    type: str = Field(..., description="Alert type (e.g. missing_document, deadline_warning, renewal_reminder)")
    message: str = Field(..., description="Actionable reminder text")
    due_date: Optional[str] = Field(None, description="Due date if applicable (YYYY-MM-DD)")

class CitizenOneFinalResponse(BaseModel):
    """Unified response containing multi-agent pipeline outputs and logging metrics."""
    extracted_data: ExtractedDocumentSchema
    eligibility: EligibilitySchema
    recommendations: RecommendationResponseSchema
    explanation: str
    notifications: List[NotificationSchema]
    
    # Activity Console tracing fields
    execution_logs: List[str] = Field(default_factory=list, description="Trace log of active agent execution steps")
    matching_criteria: List[str] = Field(default_factory=list, description="List of criteria successfully validated")
    missing_requirements: List[str] = Field(default_factory=list, description="List of unmet criteria or documents")
    documents_utilized: List[str] = Field(default_factory=list, description="List of source document types processed")
