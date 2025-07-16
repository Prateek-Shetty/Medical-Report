from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId
from datetime import datetime

router = APIRouter()

class PatientCreate(BaseModel):
    full_name: str
    email: EmailStr
    age: int
    gender: str
    condition: Optional[str] = ""

@router.post("/add")
async def add_patient(patient: PatientCreate, request: Request):
    db = request.app.state.db
    existing = await db.patients.find_one({"email": patient.email})
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists")

    patient_doc = patient.dict()
    patient_doc["created_at"] = datetime.utcnow()
    result = await db.patients.insert_one(patient_doc)
    return {"message": "Patient added", "id": str(result.inserted_id)}

@router.get("/")
async def get_all_patients(request: Request):
    db = request.app.state.db
    patients = await db.patients.find().to_list(100)
    for pat in patients:
        pat["_id"] = str(pat["_id"])
    return patients

@router.get("/{patient_id}")
async def get_patient(patient_id: str, request: Request):
    db = request.app.state.db
    patient = await db.patients.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient["_id"] = str(patient["_id"])
    return patient
