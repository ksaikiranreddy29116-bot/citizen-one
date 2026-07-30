import pytest
import asyncio
from backend.app.schemas.document import ExtractedDocumentSchema
from backend.app.agents.eligibility_agent import parse_age, run_eligibility_agent

def test_parse_age_valid_formats():
    assert parse_age("1990-05-15") == 36
    assert parse_age("15-05-1990") == 36
    assert parse_age("Born in 1995") == 31
    assert parse_age(None) is None
    assert parse_age("invalid-date") is None

@pytest.mark.asyncio
async def test_eligibility_agent_pass():
    data = ExtractedDocumentSchema(
        full_name="Rajesh Kumar",
        dob="1990-01-01",
        income_annual=250000.0,
        state="Tamil Nadu",
        document_type="Income Certificate"
    )
    eligibility = await run_eligibility_agent(data)
    assert eligibility.eligible is True
    assert len(eligibility.failed_rules) == 0
    assert "passed successfully" in eligibility.validation_reason.lower()

@pytest.mark.asyncio
async def test_eligibility_agent_fail_high_income():
    data = ExtractedDocumentSchema(
        full_name="Priya Sharma",
        dob="1995-03-10",
        income_annual=750000.0,  # Exceeds 5 Lakh cap
        state="Maharashtra",
        document_type="PAN"
    )
    eligibility = await run_eligibility_agent(data)
    assert eligibility.eligible is False
    assert "Income Ceiling" in eligibility.failed_rules
