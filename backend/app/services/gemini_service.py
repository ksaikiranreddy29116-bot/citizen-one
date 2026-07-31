import os
import json
import base64
from pathlib import Path
from typing import Type, TypeVar
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

T = TypeVar("T", bound=BaseModel)

def get_llm_client() -> OpenAI:
    """Helper to fetch initialized OpenAI-compatible client for Groq API."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            f"GROQ_API_KEY is missing from environment. Checked path: {env_path}"
        )
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )

def call_vision_ocr(image_bytes: bytes, response_schema: Type[T]) -> T:
    """
    Performs OCR and detail extraction on document images via Qwen 3.6 27B vision model on Groq.
    Includes fallbacks to handle model limitations.
    """
    client = get_llm_client()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    prompt = (
        "You are an expert OCR document processing agent for CitizenOne. "
        "Examine this document image carefully and extract applicant details into structured JSON matching the schema. "
        "Do not invent information; populate null for fields you cannot read or find."
    )
    
    # We use qwen/qwen3.6-27b as llama-3.2 vision models are decommissioned on Groq
    model_name = "qwen/qwen3.6-27b"
    
    try:
        # standard JSON object response format is highly compatible
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt + f"\nOutput MUST be valid JSON conforming to keys: {list(response_schema.model_fields.keys())}"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return response_schema.model_validate(data)
    except Exception as e:
        print(f"⚠️ Standard Vision OCR failed: {e}. Attempting beta.chat.completions.parse...")
        try:
            response = client.beta.chat.completions.parse(
                model=model_name,
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
                response_format=response_schema
            )
            return response.choices[0].message.parsed
        except Exception as parse_err:
            print(f"❌ Both Vision OCR methods failed: {parse_err}")
            raise parse_err

def call_chat_completion(
    prompt: str,
    response_schema: Type[T],
    model: str = "llama-3.3-70b-versatile"
) -> T:
    """
    Sends text prompting to Groq LLM and parses the response into the requested Pydantic schema.
    """
    client = get_llm_client()
    try:
        # Standard structured completions for Llama
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format=response_schema
        )
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"⚠️ beta.chat.completions.parse failed: {e}. Attempting standard completion with JSON format...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt + f"\nOutput MUST be valid JSON conforming to keys: {list(response_schema.model_fields.keys())}"}],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            return response_schema.model_validate(data)
        except Exception as fb_err:
            print(f"❌ Both chat completion methods failed: {fb_err}")
            raise fb_err
