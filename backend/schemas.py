from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

# =====================================================
# USER PROFILE
# =====================================================

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


# =====================================================
# USER DOCUMENT
# =====================================================

class UserDocumentCreate(BaseModel):
    user_id: int
    document_type: str
    s3_url: Optional[str] = None


class UserDocumentResponse(UserDocumentCreate):
    id: int
    verification_status: bool

    class Config:
        from_attributes = True


class UserDocumentUploadResponse(BaseModel):
    id: int
    filename: str
    s3_url: str
    verification_status: bool

    class Config:
        from_attributes = True


# =====================================================
# GOVERNMENT SCHEME
# =====================================================

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


# =====================================================
# SCHEME APPLICATION
# =====================================================

class SchemeApplicationCreate(BaseModel):
    user_id: int
    scheme_id: int


class SchemeApplicationResponse(BaseModel):
    id: int
    user_id: int
    scheme_id: int
    application_status: str
    applied_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# NOTIFICATION
# =====================================================

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str


class NotificationResponse(NotificationCreate):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# AI RECOMMENDATION
# =====================================================

class Recommendation(BaseModel):
    scheme_name: str
    category: str
    benefits: str
    match_score: int


class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]


# =====================================================
# DASHBOARD
# =====================================================

class DashboardResponse(BaseModel):
    user: UserProfileResponse
    documents: List[UserDocumentUploadResponse]
    applications: List[SchemeApplicationResponse]
    notifications: List[NotificationResponse]