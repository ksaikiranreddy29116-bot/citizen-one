from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    age = Column(Integer)

    gender = Column(String(20))

    phone = Column(String(20), unique=True)

    email = Column(String(100), unique=True)

    education_level = Column(String(100))

    occupation = Column(String(100))

    state = Column(String(100))

    district = Column(String(100))

    annual_income = Column(Float)

    caste_category = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship(
        "UserDocument",
        back_populates="user",
        cascade="all, delete"
    )


class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user_profiles.id"))

    document_type = Column(String(100))

    s3_url = Column(Text)

    verification_status = Column(Boolean, default=False)

    extracted_data = Column(JSONB)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="documents")


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    id = Column(Integer, primary_key=True, index=True)

    scheme_name = Column(String(200), nullable=False)

    category = Column(String(100))

    state = Column(String(100))

    description = Column(Text)

    eligibility = Column(Text)

    benefits = Column(Text)

    deadline = Column(Date)