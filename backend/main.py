from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from groq_client import get_scheme_recommendations

import boto3
import os
import traceback
from dotenv import load_dotenv

import models
import schemas

from database import engine, Base, get_db

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------
load_dotenv()

print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_REGION:", os.getenv("AWS_REGION"))
print("AWS_BUCKET_NAME:", os.getenv("AWS_BUCKET_NAME"))

# ----------------------------------------------------
# Create Database Tables
# ----------------------------------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------------------------------
# AWS S3 Client
# ----------------------------------------------------
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------
app = FastAPI(
    title="CitizenOne API",
    description="Backend API for CitizenOne Government Scheme Recommendation Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Home
# ----------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to CitizenOne API 🚀"
    }

# ----------------------------------------------------
# Register User
# ----------------------------------------------------
@app.post("/register", response_model=schemas.UserProfileResponse)
def register_user(
    user: schemas.UserProfileCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(models.UserProfile).filter(
        models.UserProfile.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.UserProfile(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ----------------------------------------------------
# Get Users
# ----------------------------------------------------
@app.get("/users", response_model=list[schemas.UserProfileResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.UserProfile).all()

# ----------------------------------------------------
# Add Government Scheme
# ----------------------------------------------------
@app.post("/schemes", response_model=schemas.GovernmentSchemeResponse)
def add_scheme(
    scheme: schemas.GovernmentSchemeCreate,
    db: Session = Depends(get_db)
):
    new_scheme = models.GovernmentScheme(**scheme.model_dump())

    db.add(new_scheme)
    db.commit()
    db.refresh(new_scheme)

    return new_scheme

# ----------------------------------------------------
# Get Government Schemes
# ----------------------------------------------------
@app.get("/schemes", response_model=list[schemas.GovernmentSchemeResponse])
def get_schemes(db: Session = Depends(get_db)):
    return db.query(models.GovernmentScheme).all()

# ----------------------------------------------------
# Upload Document to AWS S3
# ----------------------------------------------------
@app.post("/api/v1/documents/upload")
async def upload_document(
    user_id: int,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:

        # Read uploaded file
        file_bytes = await file.read()

        # Upload to AWS S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"uploads/{file.filename}",
            Body=file_bytes,
            ContentType=file.content_type
        )

        print("Uploaded to S3 Successfully")

        # Generate S3 URL
        s3_url = (
            f"https://{BUCKET_NAME}.s3."
            f"{os.getenv('AWS_REGION')}.amazonaws.com/uploads/{file.filename}"
        )

        # Save metadata into PostgreSQL
        new_document = models.UserDocument(
            user_id=user_id,
            document_type=document_type,
            filename=file.filename,
            s3_url=s3_url,
            verification_status=False,
            extracted_data={
                "status": "Pending Verification"
            }
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        return {
            "status": "success",
            "message": "Document uploaded successfully",
            "document_id": new_document.id,
            "filename": file.filename,
            "document_type": document_type,
            "s3_url": s3_url,
            "verification_status": False
        }

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    
@app.post("/apply", response_model=schemas.SchemeApplicationResponse)
def apply_scheme(
    application: schemas.SchemeApplicationCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(models.SchemeApplication).filter(
        models.SchemeApplication.user_id == application.user_id,
        models.SchemeApplication.scheme_id == application.scheme_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already applied for this scheme."
        )

    new_application = models.SchemeApplication(
        user_id=application.user_id,
        scheme_id=application.scheme_id,
        application_status="Pending"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    # Automatically create a notification
    notification = models.Notification(
        user_id=application.user_id,
        title="Application Submitted",
        message="Your application has been submitted successfully and is under review."
    )

    db.add(notification)
    db.commit()

    return new_application

# ----------------------------------------------------
# Get User Applications
# ----------------------------------------------------

@app.get(
    "/applications/{user_id}",
    response_model=list[schemas.SchemeApplicationResponse]
)
def get_applications(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(models.SchemeApplication).filter(
        models.SchemeApplication.user_id == user_id
    ).all()


# ----------------------------------------------------
# Create Notification
# ----------------------------------------------------

@app.post(
    "/notifications",
    response_model=schemas.NotificationResponse
)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):

    new_notification = models.Notification(
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


# ----------------------------------------------------
# Get Notifications
# ----------------------------------------------------

@app.get(
    "/notifications/{user_id}",
    response_model=list[schemas.NotificationResponse]
)
def get_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(models.Notification).filter(
        models.Notification.user_id == user_id
    ).order_by(
        models.Notification.created_at.desc()
    ).all()


# ----------------------------------------------------
# Dashboard API
# ----------------------------------------------------
@app.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):

    total_users = db.query(models.UserProfile).count()
    total_schemes = db.query(models.GovernmentScheme).count()
    total_documents = db.query(models.UserDocument).count()
    total_applications = db.query(models.SchemeApplication).count()
    total_notifications = db.query(models.Notification).count()

    return {
        "total_users": total_users,
        "total_schemes": total_schemes,
        "total_documents": total_documents,
        "total_applications": total_applications,
        "total_notifications": total_notifications
    }

@app.get(
    "/dashboard/{user_id}",
    response_model=schemas.DashboardResponse
)
def dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.UserProfile).filter(
        models.UserProfile.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    documents = db.query(models.UserDocument).filter(
        models.UserDocument.user_id == user_id
    ).all()

    applications = db.query(models.SchemeApplication).filter(
        models.SchemeApplication.user_id == user_id
    ).all()

    notifications = db.query(models.Notification).filter(
        models.Notification.user_id == user_id
    ).all()

    return {
        "user": user,
        "documents": documents,
        "applications": applications,
        "notifications": notifications
    }


@app.get("/recommendations/{user_id}")
def recommend_schemes(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.UserProfile).filter(
        models.UserProfile.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    schemes = db.query(models.GovernmentScheme).all()

    result = get_scheme_recommendations(user, schemes)

    return result
# ----------------------------------------------------
# Dashboard Statistics
# ----------------------------------------------------

