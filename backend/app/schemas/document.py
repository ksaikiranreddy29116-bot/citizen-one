from pydantic import BaseModel, Field
from typing import Optional, List

class ExtractedDocumentSchema(BaseModel):
    """Schema for document OCR extraction output."""
    full_name: Optional[str] = Field(None, description="Extracted citizen full name")
    dob: Optional[str] = Field(None, description="Date of birth in YYYY-MM-DD format")
    gender: Optional[str] = Field(None, description="Gender of the citizen")
    aadhaar_number: Optional[str] = Field(None, description="Extracted Aadhaar card number")
    income_annual: Optional[float] = Field(None, description="Annual household/individual income in INR as float")
    state: Optional[str] = Field(None, description="State of residence (e.g., Tamil Nadu, Maharashtra)")
    district: Optional[str] = Field(None, description="District of residence")
    document_type: str = Field(..., description="Detected ID type (e.g., Income Certificate, PAN, Driving License)")
    missing_fields: List[str] = Field(
        default_factory=list, 
        description="Fields required for welfare evaluation that were illegible or absent"
    )
