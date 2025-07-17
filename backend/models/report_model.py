from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Report(BaseModel):
    filename: str
    extracted_text: str
    gemini_result: str
    timestamp: Optional[datetime]
