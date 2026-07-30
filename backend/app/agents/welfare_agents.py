"""
CitizenOne - Welfare Agents Module
Powered by Groq Cloud API
"""

import os
import base64
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

# Explicitly load environment variables from backend/.env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# ==========================================
# 1. PYDANTIC SCHEMAS
# ==========================================

class ExtractedDocumentSchema(BaseModel):
    """Schema for document OCR extraction output."""
    full_name: Optional[str] = Field(None, description="Extracted citizen full name")
    dob: Optional[str] = Field(None, description="Date of birth in YYYY-MM-DD format")
    income_annual: Optional[float] = Field(None, description="Annual household/individual income in INR as float")
    state: Optional[str] = Field(None, description="State of residence (e.g., Tamil Nadu, Maharashtra)")
    document_type: str = Field(..., description="Detected ID type (e.g., Income Certificate, PAN, Driving License)")
    missing_fields: List[str] = Field(
        default_factory=list, 
        description="Fields required for welfare evaluation that were illegible or absent"
    )


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


# ==========================================
# 2. HELPER CLIENT INITIALIZATION
# ==========================================

def get_groq_client() -> OpenAI:
    """Helper function to fetch the Groq API key dynamically."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            f"GROQ_API_KEY is missing! Please verify your API key is in {env_path}"
        )
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )


# ==========================================
# 3. PHASE 2: VISION EXTRACTION AGENT (GROQ)
# ==========================================

async def run_document_autofill_agent(image_bytes: bytes) -> ExtractedDocumentSchema:
    """
    Extracts structured user data from government document images via Groq Vision API.
    """
    try:
        client = get_groq_client()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        prompt = (
            "You are an expert OCR document processing agent for CitizenOne. "
            "Examine this document image carefully and extract applicant details into the structured JSON output format. "
            "Populate null for any field that cannot be identified with certainty. "
            "List unreadable or missing fields in missing_fields."
        )

        response = client.beta.chat.completions.parse(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format=ExtractedDocumentSchema,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        print(f"❌ Groq Vision Agent Error: {e}")
        return ExtractedDocumentSchema(
            document_type="Unknown / Read Error",
            missing_fields=["full_name", "dob", "income_annual", "state"]
        )


# ==========================================
# 4. PHASE 1: SCHEME RECOMMENDATION AGENT (GROQ)
# ==========================================

async def run_scheme_recommendation_agent(
    citizen_data: ExtractedDocumentSchema
) -> RecommendationResponseSchema:
    """
    Evaluates extracted citizen details against welfare criteria using Groq.
    """
    try:
        client = get_groq_client()

        prompt = f"""
        You are the Welfare Recommendation Agent for CitizenOne.
        Evaluate the following citizen profile against standard social welfare schemes:

        CITIZEN PROFILE:
        {citizen_data.model_dump_json(indent=2)}

        EVALUATION INSTRUCTIONS:
        Evaluate eligibility for these baseline welfare categories:
        1. Low Income Assistance (Eligibility: annual income < 300000 INR)
        2. Senior Citizen Welfare (Eligibility: age >= 60 based on DOB)
        3. State Housing Allowance (Eligibility: valid state residence & income < 500000 INR)

        Return a clear evaluation adhering strictly to the required schema structure.
        """

        response = client.beta.chat.completions.parse(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format=RecommendationResponseSchema,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        print(f"❌ Groq Recommendation Agent Error: {e}")
        return RecommendationResponseSchema(
            citizen_name=citizen_data.full_name,
            recommended_schemes=[],
            next_steps=["Manual verification required due to processing error."]
        )