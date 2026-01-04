"""Feedback document model."""
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from bson import ObjectId


class FeedbackItem(BaseModel):
    """Feedback item embedded model."""
    question: str
    answer: str
    user_answer: str = Field(alias="userAnswer")
    rating: int
    feedback: str
    positive_reinforcement: Optional[str] = Field(None, alias="positiveReinforcement")
    
    model_config = ConfigDict(populate_by_name=True)


class Feedback(Document):
    """Feedback document schema."""
    sid: PydanticObjectId
    uid: PydanticObjectId
    feedbacks: List[FeedbackItem]
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "feedbacks"
        indexes = [
            ("sid", "uid"),  # Compound index for unique story-user feedback
            "sid",
            "uid",
        ]

