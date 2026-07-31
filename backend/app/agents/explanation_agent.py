from pydantic import BaseModel, Field
from app.schemas.document import ExtractedDocumentSchema
from app.schemas.eligibility import EligibilitySchema
from app.schemas.recommendation import RecommendationResponseSchema
from app.services.gemini_service import call_chat_completion
from app.prompts import get_explanation_prompt

class ExplanationSchema(BaseModel):
    explanation: str = Field(..., description="Warm, friendly, conversational explanation of citizen eligibility and recommendations.")

async def run_explanation_agent(
    citizen_data: ExtractedDocumentSchema,
    eligibility: EligibilitySchema,
    recommendations: RecommendationResponseSchema
) -> str:
    """
    Generates a conversational, citizen-friendly explanation of why they qualified
    or failed to qualify for various welfare programs.
    """
    try:
        prompt = get_explanation_prompt(
            full_name=citizen_data.full_name or 'Applicant',
            state=citizen_data.state or 'Not specified',
            income_annual=citizen_data.income_annual or 0.0,
            dob=citizen_data.dob or 'Not specified',
            is_eligible=eligibility.eligible,
            failed_rules=eligibility.failed_rules,
            validation_reason=eligibility.validation_reason,
            recommendations_json=recommendations.model_dump_json(indent=2)
        )

        parsed = call_chat_completion(
            prompt=prompt,
            response_schema=ExplanationSchema,
            model="llama-3.3-70b-versatile"
        )
        return parsed.explanation
    except Exception as e:
        print(f"❌ Explanation Agent Error: {e}")
        return (
            f"Based on your profile with an annual income of ₹{citizen_data.income_annual or 0:,.2f} "
            f"and state of {citizen_data.state or 'unknown'}, you have been reviewed for available welfare schemes. "
            "Please check the recommendation list below for details."
        )
