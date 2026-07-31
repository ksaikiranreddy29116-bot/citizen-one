from pydantic import BaseModel, Field
from typing import List
from app.schemas.document import ExtractedDocumentSchema
from app.schemas.recommendation import RecommendationResponseSchema
from app.schemas.response import NotificationSchema
from app.services.gemini_service import call_chat_completion
from app.prompts import get_notification_prompt

class NotificationListSchema(BaseModel):
    notifications: List[NotificationSchema] = Field(default_factory=list)

async def run_notification_agent(
    citizen_data: ExtractedDocumentSchema,
    recommendations: RecommendationResponseSchema
) -> List[NotificationSchema]:
    """
    Generates actionable notifications and reminders for the citizen
    such as missing documents, registration deadlines, and renewal dates.
    """
    try:
        prompt = get_notification_prompt(
            document_type=citizen_data.document_type,
            missing_fields=citizen_data.missing_fields,
            recommendations_json=recommendations.model_dump_json(indent=2)
        )

        parsed = call_chat_completion(
            prompt=prompt,
            response_schema=NotificationListSchema,
            model="llama-3.3-70b-versatile"
        )
        return parsed.notifications
    except Exception as e:
        print(f"❌ Notification Agent Error: {e}")
        fallbacks = []
        if citizen_data.missing_fields:
            fallbacks.append(NotificationSchema(
                type="missing_document",
                message=f"Please upload supporting certificates for missing fields: {', '.join(citizen_data.missing_fields)}.",
                due_date="2026-08-30"
            ))
        else:
            fallbacks.append(NotificationSchema(
                type="application_status",
                message="Welfare scheme matching completed. Please review next steps under recommended schemes.",
                due_date=None
            ))
        return fallbacks
