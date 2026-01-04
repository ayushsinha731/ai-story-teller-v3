"""Assignment document model."""
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from bson import ObjectId


class Question(BaseModel):
    """Question embedded model."""
    question: str
    answer: str
    user_answer: Optional[str] = None


class Assignment(Document):
    """Assignment document schema."""
    sid: PydanticObjectId
    uid: PydanticObjectId
    questions: List[Question]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "assignments"
        indexes = [
            ("sid", "uid"),  # Compound index for unique story-user assignments
            "sid",
            "uid",
        ]

