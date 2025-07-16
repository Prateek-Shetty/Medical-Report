from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from app.core.ai import analyze_report
from bson import ObjectId
import os
import aiofiles
import tempfile

router = APIRouter()

UPLOAD_DIR = "uploaded_reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-report")
async def upload_report(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    try:
        ai_result = await analyze_report(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

    report_doc = {
        "filename": file.filename,
        "ai_summary": ai_result,
        "path": file_path
    }
    db = request.app.state.db
    result = await db.reports.insert_one(report_doc)
    return {"report_id": str(result.inserted_id), "ai_summary": ai_result}

@router.get("/")
async def get_all_reports(request: Request):
    db = request.app.state.db
    reports = await db.reports.find().to_list(length=None)
    for report in reports:
        report["_id"] = str(report["_id"])
    return reports

