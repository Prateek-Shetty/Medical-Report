from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId
from datetime import datetime

router = APIRouter()

class DoctorCreate(BaseModel):
    full_name: str
    email: EmailStr
    specialization: str
    experience: Optional[int] = 0
    bio: Optional[str] = ""

@router.post("/add")
async def add_doctor(doctor: DoctorCreate, request: Request):
    db = request.app.state.db
    existing = await db.doctors.find_one({"email": doctor.email})
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already exists")

    doctor_doc = doctor.dict()
    doctor_doc["created_at"] = datetime.utcnow()
    result = await db.doctors.insert_one(doctor_doc)
    return {"message": "Doctor added", "id": str(result.inserted_id)}

@router.get("/")
async def get_all_doctors(request: Request):
    db = request.app.state.db
    doctors = await db.doctors.find().to_list(100)
    for doc in doctors:
        doc["_id"] = str(doc["_id"])
    return doctors

@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str, request: Request):
    db = request.app.state.db
    doctor = await db.doctors.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor["_id"] = str(doctor["_id"])
    return doctor
