import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Auto-Fill Agent (Simulated for local testing)
def run_document_autofill_agent(image_path: str = None) -> dict:
    return {
        "fullName": "Rahul Kumar",
        "annualIncome": 120000,
        "college": "VIT AP University",
        "casteCategory": "OBC",
        "state": "Andhra Pradesh"
    }

# 2. Scheme Recommendation & Eligibility Agent
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
        # Fallback dummy data if API fails
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

# 3. Reminder Agent
def run_reminder_agent(user_profile: dict) -> list:
    return [
        {
            "id": "notif-01",
            "type": "deadline",
            "message": "NSP Post-Matric Scholarship deadline closes in 6 days!"
        }
    ]