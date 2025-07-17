# backend/routes/report.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from config.db import report_collection
from services.pdf_utils import extract_text  # Unified function
from services.gemini_api import analyze_text_with_gemini
from datetime import datetime
import base64

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename
        base64_data = base64.b64encode(contents).decode("utf-8")

        # Extract text from uploaded file (PDF or image)
        extracted_text = extract_text(contents, filename)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted.")

        # Analyze using Gemini
        gemini_result = analyze_text_with_gemini(extracted_text)

        # Create MongoDB document
        doc = {
            "filename": filename,
            "file_data": base64_data,
            "extracted_text": extracted_text,
            "gemini_result": gemini_result,
            "timestamp": datetime.utcnow()
        }

        # Insert into MongoDB
        inserted = report_collection.insert_one(doc)

        return {
            "report_id": str(inserted.inserted_id),
            "gemini_result": gemini_result
        }

    except Exception as e:
        print("❌ Upload processing failed:", e)
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
