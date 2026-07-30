from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_scheme_recommendations(user, schemes):

    scheme_text = ""

    for scheme in schemes:
        scheme_text += f"""
Scheme Name: {scheme.scheme_name}
Category: {scheme.category}
Eligibility: {scheme.eligibility}
Benefits: {scheme.benefits}

"""

    prompt = f"""
You are an AI Government Welfare Advisor.

User Profile

Name: {user.full_name}
Age: {user.age}
Gender: {user.gender}
Education: {user.education_level}
Occupation: {user.occupation}
State: {user.state}
District: {user.district}
Annual Income: {user.annual_income}
Category: {user.caste_category}

Government Schemes

{scheme_text}

Recommend ONLY the best matching government schemes.

Return ONLY valid JSON.

Do NOT write explanations before or after the JSON.
Do NOT use markdown.
Do NOT use ```json.

Return exactly in this format:

[
    {{
        "scheme_name": "",
        "match_score": 95,
        "reason": ""
    }}
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()

    # Remove markdown code blocks if Groq still returns them
    result = re.sub(r"```json|```", "", result).strip()

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_response": result
        }