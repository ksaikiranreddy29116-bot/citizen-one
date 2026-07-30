from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, Base, get_db

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="CitizenOne API",
    description="Backend API for CitizenOne Government Scheme Recommendation Platform",
    version="1.0.0"
)

# -------------------------
# Home Route
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to CitizenOne API 🚀"
    }

# -------------------------
# Register User
# -------------------------

@app.post("/register", response_model=schemas.UserProfileResponse)
def register_user(
    user: schemas.UserProfileCreate,
    db: Session = Depends(get_db)
):

    existing_email = db.query(models.UserProfile).filter(
        models.UserProfile.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.UserProfile(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# -------------------------
# Get All Users
# -------------------------

@app.get("/users", response_model=list[schemas.UserProfileResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.UserProfile).all()

# -------------------------
# Add Government Scheme
# -------------------------

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

# -------------------------
# Get All Government Schemes
# -------------------------

@app.get("/schemes", response_model=list[schemas.GovernmentSchemeResponse])
def get_schemes(db: Session = Depends(get_db)):
    return db.query(models.GovernmentScheme).all()