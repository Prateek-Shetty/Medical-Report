from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.shared import PyObjectId

class Report(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    patient_id: str
    doctor_id: str
    file_name: str
    file_path: str
    summary: Optional[str] = None
    issues: Optional[str] = None
    suggestions: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
