import json
import os
from app.agents.graph_manager import citizen_one_pipeline
from app.agents.welfare_agents import run_document_autofill_agent

dummy_user = {
    "income": 120000,
    "occupation": "Student",
    "state": "Andhra Pradesh",
    "education": "Undergraduate"
}

print("⚡ Testing CitizenOne Multi-Agent Engine with Live Vision Extraction...\n")

# 1. Test LangGraph Orchestrator
result = citizen_one_pipeline.invoke({"user_profile": dummy_user})

print("--- [1] SCHEME RECOMMENDATIONS JSON ---")
print(json.dumps(result["recommendations"], indent=2))

# 2. Test Live Gemini Vision Extraction
sample_img_path = "sample_doc.jpg"

if os.path.exists(sample_img_path):
    print(f"\n--- [2] LIVE VISION EXTRACTION FROM {sample_img_path} ---")
    autofill_res = run_document_autofill_agent(sample_img_path)
else:
    print("\n--- [2] FALLBACK AUTO-FILL (No sample_doc.jpg found) ---")
    autofill_res = run_document_autofill_agent()

print(json.dumps(autofill_res, indent=2))