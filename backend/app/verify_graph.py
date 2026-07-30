import asyncio
import json
import os
import sys
from pathlib import Path

# Force stdout/stderr to use UTF-8 to prevent charmap/UnicodeEncodeError on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add project root to path so we can import app modules
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from app.agents.orchestrator_agent import run_citizen_pipeline
from app.schemas.document import ExtractedDocumentSchema

async def main():
    print("[INFO] Initiating local multi-agent pipeline verification...\n")
    
    # 1. Verification with document image (full pipeline)
    sample_img_path = Path(__file__).resolve().parent.parent / "sample_doc.jpeg"
    if not sample_img_path.exists():
        print(f"[ERROR] {sample_img_path} not found.")
        sys.exit(1)
        
    print(f"Executing pipeline with image: {sample_img_path}")
    with open(sample_img_path, "rb") as f:
        img_bytes = f.read()
        
    try:
        response = await run_citizen_pipeline(document_bytes=img_bytes)
        
        print("\n=============================================")
        print("CITIZENONE MULTI-AGENT RESPONSE VERIFICATION")
        print("=============================================\n")
        
        print("--- EXTRACTED DATA ---")
        print(json.dumps(response.extracted_data.model_dump(), indent=2))
        
        print("\n--- ELIGIBILITY REPORT ---")
        print(json.dumps(response.eligibility.model_dump(), indent=2))
        
        print("\n--- SCHEME RECOMMENDATIONS ---")
        print(json.dumps(response.recommendations.model_dump(), indent=2))
        
        print("\n--- CONVERSATIONAL EXPLANATION ---")
        print(response.explanation)
        
        print("\n--- CALENDAR NOTIFICATIONS ---")
        print(json.dumps([n.model_dump() for n in response.notifications], indent=2))
        
        print("\n--- AGENT ACTIVITY TRACE LOGS ---")
        for idx, log in enumerate(response.execution_logs, 1):
            print(f"{idx:02d}. {log}")
            
        print("\n--- TRACE METRICS ---")
        print(f"Documents Utilized: {response.documents_utilized}")
        print(f"Matching Criteria: {response.matching_criteria}")
        print(f"Missing Requirements: {response.missing_requirements}")
        
        # Validation checks
        print("\n--- INTEGRITY CHECKS ---")
        assert response.extracted_data.document_type != "Unknown / Read Error", "OCR extraction failed to parse document."
        assert len(response.execution_logs) > 0, "No execution trace logs generated."
        assert len(response.explanation) > 0, "No explanation generated."
        print("[SUCCESS] All multi-agent integrity validations passed!")
        
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
