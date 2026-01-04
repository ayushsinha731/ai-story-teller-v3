"""Pydantic models for feedback requests and responses."""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class FeedbackItem(BaseModel):
    """Feedback item model."""
    question: str
    answer: str
    user_answer: str = Field(..., alias="userAnswer")
    rating: int
    feedback: str
    positive_reinforcement: Optional[str] = Field(None, alias="positiveReinforcement")


class FeedbackRequest(BaseModel):
    """Feedback request model."""
    answers: List[str] = Field(..., min_items=5, max_items=5, description="List of 5 answers")


class FeedbackResponse(BaseModel):
    """Feedback response model."""
    id: str
    sid: str
    uid: str
    feedbacks: List[FeedbackItem]
    
    model_config = ConfigDict(from_attributes=True)

