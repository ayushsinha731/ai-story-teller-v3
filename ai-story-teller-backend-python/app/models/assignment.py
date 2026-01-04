"""Pydantic models for assignment requests and responses."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class Question(BaseModel):
    """Question model."""
    question: str
    answer: str
    user_answer: Optional[str] = Field(None, alias="userAnswer")


class AssignmentResponse(BaseModel):
    """Assignment response model."""
    id: str
    sid: str
    uid: str
    questions: List[Question]
    
    model_config = ConfigDict(from_attributes=True)

