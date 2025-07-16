from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

router = APIRouter()

# Pydantic models
class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    date: str  # format: "YYYY-MM-DD"
    time: str  # format: "HH:MM"
    reason: Optional[str] = None

class AppointmentOut(BaseModel):
    id: str = Field(..., alias="_id")
    patient_id: str
    doctor_id: str
    date: str
    time: str
    reason: Optional[str] = None

# Utils
def to_object_id(id_str: str):
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

# Create an appointment
@router.post("/create")
async def create_appointment(data: AppointmentCreate, request: Request):
    db = request.app.state.db

    appointment = data.dict()
    appointment["created_at"] = datetime.utcnow()

    result = await db.appointments.insert_one(appointment)
    return {"message": "Appointment created", "appointment_id": str(result.inserted_id)}

# Get all appointments
@router.get("/")
async def get_appointments(request: Request):
    db = request.app.state.db
    appointments = await db.appointments.find().to_list(length=100)
    for app in appointments:
        app["_id"] = str(app["_id"])
    return appointments

# Get appointments by patient or doctor
@router.get("/user/{user_id}")
async def get_appointments_for_user(user_id: str, request: Request):
    db = request.app.state.db
    query = {"$or": [{"patient_id": user_id}, {"doctor_id": user_id}]}
    results = await db.appointments.find(query).to_list(100)
    for r in results:
        r["_id"] = str(r["_id"])
    return results

# Delete appointment
@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: str, request: Request):
    db = request.app.state.db
    result = await db.appointments.delete_one({"_id": to_object_id(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted"}
