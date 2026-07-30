import pytest
from backend.app.schemas.document import ExtractedDocumentSchema
from backend.app.schemas.eligibility import EligibilitySchema, RuleValidation
from backend.app.schemas.recommendation import SchemeMatch, RecommendationResponseSchema
from backend.app.schemas.response import NotificationSchema, CitizenOneFinalResponse

def test_extracted_document_schema():
    doc = ExtractedDocumentSchema(
        full_name="Aahil Baba",
        income_annual=150000.0,
        state="Andhra Pradesh",
        document_type="Student ID"
    )
    assert doc.full_name == "Aahil Baba"
    assert doc.missing_fields == []

def test_recommendation_schema():
    match = SchemeMatch(
        scheme_id="SCHEME_001",
        scheme_name="Low Income Assistance",
        eligible=True,
        match_score=0.95,
        reasoning=["Income below threshold"]
    )
    recs = RecommendationResponseSchema(
        citizen_name="Aahil Baba",
        recommended_schemes=[match],
        next_steps=["Apply online"]
    )
    assert len(recs.recommended_schemes) == 1
    assert recs.recommended_schemes[0].eligible is True

def test_final_response_schema():
    ext = ExtractedDocumentSchema(document_type="Aadhaar")
    elig = EligibilitySchema(eligible=True, failed_rules=[], validation_reason="Passed", rule_validations=[])
    recs = RecommendationResponseSchema(recommended_schemes=[], next_steps=[])
    
    resp = CitizenOneFinalResponse(
        extracted_data=ext,
        eligibility=elig,
        recommendations=recs,
        explanation="Test explanation",
        notifications=[NotificationSchema(type="alert", message="Test alert", due_date="2026-12-31")],
        execution_logs=["Step 1"],
        matching_criteria=["Income"],
        missing_requirements=[],
        documents_utilized=["Aadhaar"]
    )
    assert resp.extracted_data.document_type == "Aadhaar"
    assert len(resp.notifications) == 1
