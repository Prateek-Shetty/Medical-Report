import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

load_dotenv()  # Load .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY not found in environment")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    logging.error(f"❌ Failed to initialize Gemini: {e}")
    model = None

async def analyze_report(file_path: str) -> str:
    if not model:
        raise Exception("Gemini model is not initialized")

    try:
        with open(file_path, "r") as f:
            content = f.read()

        response = model.generate_content(content)
        return response.text
    except Exception as e:
        logging.error(f"Gemini content generation failed: {e}")
        raise Exception(f"Gemini API error: {e}")
