from pydantic import BaseModel, Field
from typing import List

class RuleValidation(BaseModel):
    rule_name: str
    passed: bool
    reason: str

class EligibilitySchema(BaseModel):
    eligible: bool = Field(..., description="Overall eligibility status")
    failed_rules: List[str] = Field(default_factory=list, description="List of failed rule names")
    validation_reason: str = Field(..., description="Detailed explanation of validation results")
    rule_validations: List[RuleValidation] = Field(default_factory=list, description="Individual rule check details")
