from app.schemas.document import ExtractedDocumentSchema
from app.services.gemini_service import call_vision_ocr

async def run_document_autofill_agent(image_bytes: bytes) -> ExtractedDocumentSchema:
    """
    Extracts structured user data from government document images.
    """
    try:
        extracted = call_vision_ocr(image_bytes, ExtractedDocumentSchema)
        return extracted
    except Exception as e:
        print(f"❌ Document Agent OCR Error: {e}")
        # Return fallback output to ensure the API never crashes if OCR fails
        return ExtractedDocumentSchema(
            document_type="Unknown / Read Error",
            missing_fields=["full_name", "dob", "income_annual", "state"]
        )
