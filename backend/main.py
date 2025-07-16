# main.py (placed in backend/)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

# Import routers
from app.api import auth, users, doctors, patients, appointments, reports

app = FastAPI(
    title="Hospital Management System API",
    description="Backend for Hospital/Clinic Desktop App using FastAPI + MongoDB + Gemini AI",
    version="1.0.0"
)

# Setup logging
logging.basicConfig(level=logging.INFO)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
@app.on_event("startup")
async def connect_to_mongo():
    try:
        client = AsyncIOMotorClient(settings.MONGO_URL)
        app.state.db = client[settings.DB_NAME]
        logging.info(f"✅ Connected to MongoDB → DB: {settings.DB_NAME}")
    except Exception as e:
        logging.error(f"❌ MongoDB Connection Error: {e}")

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Health check
@app.get("/")
async def root():
    return {"status": "Backend running", "db": settings.DB_NAME}
