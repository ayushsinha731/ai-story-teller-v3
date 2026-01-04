"""Story document model."""
from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId


class PageContent(BaseModel):
    """Page content embedded model."""
    page_text: str = Field(..., alias="pageText")
    page_image: Optional[str] = Field(None, alias="pageImage")
    
    class Config:
        populate_by_name = True


class Story(Document):
    """Story document schema."""
    story_title: str
    story_description: str
    story_content: List[PageContent]
    story_author: str
    created_by: Indexed(PydanticObjectId)
    max_pages: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "stories"
        indexes = [
            "created_by",
            ("created_by", "created_at"),  # Compound index for user's stories sorted by date
            "story_title",
        ]

