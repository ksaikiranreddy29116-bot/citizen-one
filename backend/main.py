import boto3
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        # Upload file directly to Amazon S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"uploads/{file.filename}",
            Body=file_bytes,
            ContentType=file.content_type
        )
        
        # S3 URL where the file is stored
        s3_url = f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/uploads/{file.filename}"
        
        return {
            "status": "success",
            "message": "Document uploaded successfully to Amazon S3",
            "filename": file.filename,
            "s3_url": s3_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 Upload Failed: {str(e)}")
    