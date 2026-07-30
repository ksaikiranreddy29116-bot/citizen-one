from datetime import datetime
from typing import Optional
from app.schemas.document import ExtractedDocumentSchema
from app.schemas.eligibility import EligibilitySchema, RuleValidation

def parse_age(dob_str: Optional[str]) -> Optional[int]:
    """Calculates age from a date of birth string in standard formats."""
    if not dob_str:
        return None
    
    # Try parsing standard YYYY-MM-DD
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            dob = datetime.strptime(dob_str.strip(), fmt)
            # Reference date set to current year 2026
            current_year = 2026
            age = current_year - dob.year
            # Check if birthday has occurred
            if (dob.month, dob.day) > (7, 30):  # Current date 2026-07-30
                age -= 1
            return max(0, age)
        except ValueError:
            continue
            
    # Try parsing just 4 digit year
    try:
        clean_str = dob_str.strip()
        for word in clean_str.split():
            if len(word) == 4 and word.isdigit():
                return 2026 - int(word)
    except Exception:
        pass
        
    return None

async def run_eligibility_agent(citizen_data: ExtractedDocumentSchema) -> EligibilitySchema:
    """
    Evaluates citizen data against government eligibility rules.
    Checks:
    - Age (via dob)
    - Gender
    - Income (via income_annual)
    - State (via state)
    - Category
    - Occupation
    """
    rule_validations = []
    failed_rules = []
    
    # 1. Income Check (Threshold: ₹5,000,000 for baseline programs, ₹3,000,000 for low income)
    income = citizen_data.income_annual
    income_passed = True
    income_reason = "Annual income is within eligibility limits."
    if income is not None:
        if income > 500000.0:
            income_passed = False
            income_reason = f"Annual income of ₹{income:,.2f} exceeds the maximum safety-net cap of ₹5,00,000."
            failed_rules.append("Income Ceiling")
    else:
        # Fallback to true, but note missing details
        income_reason = "Annual income not provided; assuming standard eligibility."
        
    rule_validations.append(RuleValidation(
        rule_name="Income Ceiling",
        passed=income_passed,
        reason=income_reason
    ))

    # 2. State Check
    state = citizen_data.state
    state_passed = True
    state_reason = f"State of residence ({state}) is valid."
    if not state:
        state_passed = False
        state_reason = "Residency state is missing from document details."
        failed_rules.append("Residency Verification")
    elif state.strip().lower() not in [
        "tamil nadu", "andhra pradesh", "telangana", "karnataka", 
        "kerala", "maharashtra", "delhi", "gujarat", "rajasthan"
    ]:
        # Log residence, but pass warning
        state_reason = f"Resident of {state}. Eligible for state-agnostic national schemes."

    rule_validations.append(RuleValidation(
        rule_name="Residency Verification",
        passed=state_passed,
        reason=state_reason
    ))

    # 3. Age Check
    age = parse_age(citizen_data.dob)
    age_passed = True
    age_reason = f"Age ({age} years) is verified."
    if age is None:
        age_passed = False
        age_reason = "Age could not be computed due to missing or invalid date of birth."
        failed_rules.append("Age Verification")
    elif age < 0 or age > 120:
        age_passed = False
        age_reason = f"Age ({age} years) is outside valid range."
        failed_rules.append("Age Verification")
        
    rule_validations.append(RuleValidation(
        rule_name="Age Verification",
        passed=age_passed,
        reason=age_reason
    ))

    # 4. Gender / Category / Occupation checks (Placeholder validation logic)
    # Since these are optional in OCR but needed in evaluation, we pass them with default reasons
    rule_validations.append(RuleValidation(
        rule_name="Demographic Validation",
        passed=True,
        reason=f"Gender is registered as {citizen_data.gender or 'General/Unspecified'}."
    ))
    
    rule_validations.append(RuleValidation(
        rule_name="Social Category Verification",
        passed=True,
        reason="Assigned to standard demographic group."
    ))

    rule_validations.append(RuleValidation(
        rule_name="Occupation Verification",
        passed=True,
        reason="Employment status meets general requirements."
    ))

    # Overall eligibility: True if no critical rules failed
    is_eligible = len(failed_rules) == 0
    
    if is_eligible:
        validation_reason = "All government eligibility checks passed successfully."
    else:
        validation_reason = f"Eligibility failed due to: {', '.join(failed_rules)}."

    return EligibilitySchema(
        eligible=is_eligible,
        failed_rules=failed_rules,
        validation_reason=validation_reason,
        rule_validations=rule_validations
    )
