from pydantic import BaseModel, Field
from typing import List, Optional

class SchemeMatch(BaseModel):
    """Schema for individual scheme evaluation result."""
    scheme_id: str = Field(..., description="Unique scheme identifier code")
    scheme_name: str = Field(..., description="Full title of government scheme")
    eligible: bool = Field(..., description="True if citizen meets basic criteria")
    match_score: float = Field(..., description="Eligibility confidence rating between 0.0 and 1.0")
    reasoning: List[str] = Field(default_factory=list, description="Specific eligibility conditions met or failed")

class RecommendationResponseSchema(BaseModel):
    """Schema for aggregated scheme recommendations."""
    citizen_name: Optional[str] = Field(None, description="Name of applicant evaluated")
    recommended_schemes: List[SchemeMatch] = Field(default_factory=list, description="Evaluated welfare schemes")
    next_steps: List[str] = Field(default_factory=list, description="Action items for citizen submission")
