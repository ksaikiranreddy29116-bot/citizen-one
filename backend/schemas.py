from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


# -------------------------
# User Profile Schemas
# -------------------------

class UserProfileCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    phone: str
    email: EmailStr
    education_level: str
    occupation: str
    state: str
    district: str
    annual_income: float
    caste_category: str


class UserProfileResponse(UserProfileCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# User Document Schemas
# -------------------------

class UserDocumentCreate(BaseModel):
    user_id: int
    document_type: str
    s3_url: Optional[str] = None


class UserDocumentResponse(UserDocumentCreate):
    id: int
    verification_status: bool

    class Config:
        from_attributes = True


# -------------------------
# Government Scheme Schemas
# -------------------------

class GovernmentSchemeCreate(BaseModel):
    scheme_name: str
    category: str
    state: str
    description: str
    eligibility: str
    benefits: str
    deadline: Optional[date] = None


class GovernmentSchemeResponse(GovernmentSchemeCreate):
    id: int

    class Config:
        from_attributes = True