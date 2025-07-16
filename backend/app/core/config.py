import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "hospital")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()
