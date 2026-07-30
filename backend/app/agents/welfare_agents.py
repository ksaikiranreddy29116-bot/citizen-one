import os
import json
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------------------------------------------------
# 1. Pydantic Schema for Structured Multimodal Extraction
# -------------------------------------------------------------
class ExtractedDocumentSchema(BaseModel):
    fullName: str
    annualIncome: int
    college: str
    casteCategory: str
    state: str

# -------------------------------------------------------------
# 2. Live Multimodal Auto-Fill Agent
# -------------------------------------------------------------
def run_document_autofill_agent(image_path: str = None) -> dict:
    """Uses Gemini 2.5 Flash Vision to extract text from an image, falling back to dummy data if no image is provided."""
    
    # Fallback if no image path is passed (for initial testing)
    if not image_path or not os.path.exists(image_path):
        return {
            "fullName": "Rahul Kumar",
            "annualIncome": 120000,
            "college": "VIT AP University",
            "casteCategory": "OBC",
            "state": "Andhra Pradesh"
        }

    try:
        # Load the uploaded image
        img = Image.open(image_path)
        
        prompt = """
        Analyze this official Indian government document or certificate.
        Extract the following fields accurately:
        - Full Name
        - Annual Income (as an integer in INR)
        - Educational Institution / College / School Name
        - Caste / Category (e.g., General, OBC, SC, ST)
        - State of Residence
        
        If a field is not present on the document, infer or return empty string / zero.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[img, prompt],
            config={
                "response_mime_type": "application/json",
                "response_schema": ExtractedDocumentSchema,
            }
        )
        return json.loads(response.text)

    except Exception as e:
        print(f"⚠️ Gemini Vision Extraction Error: {e}")
        # Return structured fallback if image parsing fails
        return {
            "fullName": "Rahul Kumar",
            "annualIncome": 120000,
            "college": "VIT AP University",
            "casteCategory": "OBC",
            "state": "Andhra Pradesh"
        }

# -------------------------------------------------------------
# 3. Scheme Recommendation & Eligibility Agent
# -------------------------------------------------------------
def run_recommendation_agent(user_profile: dict) -> dict:
    prompt = f"""
    Evaluate this user profile against Indian government schemes:
    {json.dumps(user_profile)}
    
    Return top eligible schemes.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "system_instruction": (
                    "Return JSON strictly with format: "
                    "{'recommendedSchemes': [{'id': 'SCH-AP-01', 'name': str, 'score': 95, 'reason': str}]}"
                )
            }
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "recommendedSchemes": [
                {
                    "id": "SCH-AP-01",
                    "name": "AP Vidya Deevena",
                    "score": 95,
                    "reason": "100% fee reimbursement eligibility based on AP domicile and income below ₹2.5 Lakhs."
                }
            ]
        }

# -------------------------------------------------------------
# 4. Reminder Agent
# -------------------------------------------------------------
def run_reminder_agent(user_profile: dict) -> list:
    return [
        {
            "id": "notif-01",
            "type": "deadline",
            "message": "NSP Post-Matric Scholarship deadline closes in 6 days!"
        }
    ]