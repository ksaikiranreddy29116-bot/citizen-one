import json
from app.agents.graph_manager import citizen_one_pipeline
from app.agents.welfare_agents import run_document_autofill_agent

dummy_user = {
    "income": 120000,
    "occupation": "Student",
    "state": "Andhra Pradesh",
    "education": "Undergraduate"
}

print("⚡ Running CitizenOne Multi-Agent Engine...\n")

result = citizen_one_pipeline.invoke({"user_profile": dummy_user})

print("--- [1] SCHEME RECOMMENDATIONS JSON ---")
print(json.dumps(result["recommendations"], indent=2))

print("\n--- [2] NOTIFICATIONS JSON ---")
print(json.dumps(result["notifications"], indent=2))

print("\n--- [3] FORM AUTO-FILL JSON ---")
print(json.dumps(run_document_autofill_agent(), indent=2))