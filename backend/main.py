import boto3
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import Gayatri's Database Modules
import models, schemas
from database import engine, get_db

# Automatically create database tables if they don't exist
#models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CitizenOne Backend API")

# Enable CORS for Member 1 (React UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AWS S3 Client
s3_client = boto3.client("s3", region_name="ap-south-1")
BUCKET_NAME = "citizenone-bucket"

@app.get("/")
def read_root():
    return {"status": "online", "message": "CitizenOne API with S3 & RDS integration is running!"}

# --- AWS S3 Upload + RDS Database Recording Endpoint ---
@app.post("/api/v1/documents/upload")
async def upload_document(
    citizen_name: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    try:
        # 1. Read file bytes and upload directly to Amazon S3
        file_bytes = await file.read()
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"uploads/{file.filename}",
            Body=file_bytes,
            ContentType=file.content_type
        )
        s3_url = f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/uploads/{file.filename}"

        # 2. TEMPORARILY COMMENTED OUT DATABASE SAVING FOR LOCAL S3 TESTING:
        # new_doc = models.CitizenDocument(
        #     citizen_name=citizen_name,
        #     filename=file.filename,
        #     s3_url=s3_url
        # )
        # db.add(new_doc)
        # db.commit()
        # db.refresh(new_doc)

        return {
            "status": "success",
            "message": "File uploaded to AWS S3 successfully!",
            # "document_id": new_doc.id,
            "filename": file.filename,
            "s3_url": s3_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 Upload Error: {str(e)}")