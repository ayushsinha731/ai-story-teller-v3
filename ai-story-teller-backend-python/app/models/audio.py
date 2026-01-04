"""Pydantic models for audio requests and responses."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class AudioResponse(BaseModel):
    """Audio response model."""
    id: str
    file_path: str = Field(..., alias="filePath")
    file_name: str = Field(..., alias="fileName")
    s3_key: Optional[str] = Field(None, alias="s3Key")
    s3_bucket: Optional[str] = Field(None, alias="s3Bucket")
    transcript: Optional[str] = None
    score: Optional[float] = None
    whole_story: str = Field(..., alias="wholeStory")
    sid: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AudioFeedbackResponse(BaseModel):
    """Audio feedback response model."""
    audio: AudioResponse
    story: dict

