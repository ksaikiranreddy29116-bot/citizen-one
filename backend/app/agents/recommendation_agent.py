from app.schemas.document import ExtractedDocumentSchema
from app.schemas.recommendation import RecommendationResponseSchema
from app.services.gemini_service import call_chat_completion
from app.prompts import get_recommendation_prompt

async def run_scheme_recommendation_agent(
    citizen_data: ExtractedDocumentSchema
) -> RecommendationResponseSchema:
    """
    Evaluates extracted citizen details against welfare criteria using the Groq API model.
    Uses centralized prompt templates.
    """
    try:
        prompt = get_recommendation_prompt(citizen_data.model_dump_json(indent=2))

        return call_chat_completion(
            prompt=prompt,
            response_schema=RecommendationResponseSchema,
            model="llama-3.3-70b-versatile"
        )
    except Exception as e:
        print(f"❌ Recommendation Agent Error: {e}")
        return RecommendationResponseSchema(
            citizen_name=citizen_data.full_name,
            recommended_schemes=[],
            next_steps=["Manual verification required due to processing error."]
        )
