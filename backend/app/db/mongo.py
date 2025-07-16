from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Optional: dependency to access DB in routes
def get_db(request: Request):
    return request.app.state.db
