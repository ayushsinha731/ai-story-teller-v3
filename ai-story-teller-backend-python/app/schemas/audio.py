"""Audio document model."""
from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import Optional
from bson import ObjectId


class Audio(Document):
    """Audio document schema."""
    file_path: str  # S3 URL
    file_name: str
    s3_key: Optional[str] = None  # S3 key for deletion/management
    s3_bucket: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    score: Optional[float] = None
    transcript: Optional[str] = None
    whole_story: str
    sid: Optional[PydanticObjectId] = None
    
    class Settings:
        name = "audios"
        indexes = [
            "sid",
            "created_at",
        ]

