import os
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from app.schemas.response import CitizenOneFinalResponse

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./citizen_one.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# RELATIONAL DATABASE MODELS
# ==========================================

class CitizenProfileModel(Base):
    """Citizen Demographic & Profile Persistence"""
    __tablename__ = "citizen_profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=True)
    dob = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    aadhaar_number = Column(String, nullable=True)
    income_annual = Column(Float, nullable=True)
    state = Column(String, index=True, nullable=True)
    district = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship("DocumentModel", back_populates="citizen", cascade="all, delete-orphan")
    recommendations = relationship("RecommendationModel", back_populates="citizen", cascade="all, delete-orphan")
    notifications = relationship("NotificationModel", back_populates="citizen", cascade="all, delete-orphan")
    execution_logs = relationship("ExecutionLogModel", back_populates="citizen", cascade="all, delete-orphan")


class DocumentModel(Base):
    """Processed Upload Document Metadata"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizen_profiles.id"), nullable=False)
    document_type = Column(String, nullable=False)
    missing_fields_json = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("CitizenProfileModel", back_populates="documents")


class RecommendationModel(Base):
    """Matched Government Schemes & Evaluation"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizen_profiles.id"), nullable=False)
    scheme_id = Column(String, nullable=False)
    scheme_name = Column(String, nullable=False)
    eligible = Column(Boolean, default=False)
    match_score = Column(Float, default=0.0)
    reasoning_json = Column(Text, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("CitizenProfileModel", back_populates="recommendations")


class NotificationModel(Base):
    """Citizen Action Alerts & Reminders"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizen_profiles.id"), nullable=False)
    type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    due_date = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("CitizenProfileModel", back_populates="notifications")


class ExecutionLogModel(Base):
    """AI Activity Console & Audit Tracing Logs"""
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizen_profiles.id"), nullable=False)
    trace_log_json = Column(Text, nullable=False)
    matching_criteria_json = Column(Text, nullable=True)
    missing_requirements_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("CitizenProfileModel", back_populates="execution_logs")


# Initialize Tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency provider for DB session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# CRUD HELPER FUNCTIONS
# ==========================================

def save_full_pipeline_run(response: CitizenOneFinalResponse) -> int:
    """Persists complete LangGraph multi-agent execution output to database."""
    db = SessionLocal()
    try:
        ext = response.extracted_data
        
        # 1. Create or query Citizen Profile
        citizen = CitizenProfileModel(
            full_name=ext.full_name or "Anonymous Citizen",
            dob=ext.dob,
            gender=ext.gender,
            aadhaar_number=ext.aadhaar_number,
            income_annual=ext.income_annual,
            state=ext.state,
            district=ext.district
        )
        db.add(citizen)
        db.flush()  # Get generated citizen.id
        
        # 2. Save Document metadata
        doc = DocumentModel(
            citizen_id=citizen.id,
            document_type=ext.document_type,
            missing_fields_json=json.dumps(ext.missing_fields)
        )
        db.add(doc)
        
        # 3. Save Scheme Recommendations
        for scheme in response.recommendations.recommended_schemes:
            rec = RecommendationModel(
                citizen_id=citizen.id,
                scheme_id=scheme.scheme_id,
                scheme_name=scheme.scheme_name,
                eligible=scheme.eligible,
                match_score=scheme.match_score,
                reasoning_json=json.dumps(scheme.reasoning)
            )
            db.add(rec)
            
        # 4. Save Notifications
        for notif in response.notifications:
            n = NotificationModel(
                citizen_id=citizen.id,
                type=notif.type,
                message=notif.message,
                due_date=notif.due_date
            )
            db.add(n)
            
        # 5. Save Execution Logs / Activity Traces
        log = ExecutionLogModel(
            citizen_id=citizen.id,
            trace_log_json=json.dumps(response.execution_logs),
            matching_criteria_json=json.dumps(response.matching_criteria),
            missing_requirements_json=json.dumps(response.missing_requirements)
        )
        db.add(log)
        
        db.commit()
        return citizen.id
    except Exception as e:
        print(f"❌ Error persisting pipeline run: {e}")
        db.rollback()
        return -1
    finally:
        db.close()


def get_citizen_profiles(limit: int = 50) -> List[Dict[str, Any]]:
    """Returns a list of saved citizen profiles."""
    db = SessionLocal()
    try:
        profiles = db.query(CitizenProfileModel).order_by(CitizenProfileModel.created_at.desc()).limit(limit).all()
        return [
            {
                "id": p.id,
                "full_name": p.full_name,
                "state": p.state,
                "income_annual": p.income_annual,
                "created_at": p.created_at.isoformat()
            }
            for p in profiles
        ]
    finally:
        db.close()


def get_citizen_history(citizen_id: int) -> Optional[Dict[str, Any]]:
    """Returns complete evaluation history for a given citizen profile."""
    db = SessionLocal()
    try:
        profile = db.query(CitizenProfileModel).filter(CitizenProfileModel.id == citizen_id).first()
        if not profile:
            return None
            
        return {
            "citizen_id": profile.id,
            "full_name": profile.full_name,
            "dob": profile.dob,
            "income_annual": profile.income_annual,
            "state": profile.state,
            "documents": [
                {"document_type": d.document_type, "missing_fields": json.loads(d.missing_fields_json or "[]")}
                for d in profile.documents
            ],
            "recommendations": [
                {
                    "scheme_id": r.scheme_id,
                    "scheme_name": r.scheme_name,
                    "eligible": r.eligible,
                    "match_score": r.match_score,
                    "reasoning": json.loads(r.reasoning_json or "[]")
                }
                for r in profile.recommendations
            ],
            "notifications": [
                {"type": n.type, "message": n.message, "due_date": n.due_date}
                for n in profile.notifications
            ]
        }
    finally:
        db.close()


def get_all_execution_logs(limit: int = 20) -> List[Dict[str, Any]]:
    """Returns AI Activity Console trace logs across runs."""
    db = SessionLocal()
    try:
        logs = db.query(ExecutionLogModel).order_by(ExecutionLogModel.created_at.desc()).limit(limit).all()
        return [
            {
                "id": l.id,
                "citizen_id": l.citizen_id,
                "execution_logs": json.loads(l.trace_log_json),
                "matching_criteria": json.loads(l.matching_criteria_json or "[]"),
                "missing_requirements": json.loads(l.missing_requirements_json or "[]"),
                "created_at": l.created_at.isoformat()
            }
            for l in logs
        ]
    finally:
        db.close()


def get_all_notifications(limit: int = 50) -> List[Dict[str, Any]]:
    """Returns all citizen notifications and calendar alerts."""
    db = SessionLocal()
    try:
        notifs = db.query(NotificationModel).order_by(NotificationModel.created_at.desc()).limit(limit).all()
        return [
            {
                "id": n.id,
                "citizen_id": n.citizen_id,
                "type": n.type,
                "message": n.message,
                "due_date": n.due_date,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat()
            }
            for n in notifs
        ]
    finally:
        db.close()
