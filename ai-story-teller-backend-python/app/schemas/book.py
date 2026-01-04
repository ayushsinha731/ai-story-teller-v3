"""Book document model."""
from beanie import Document, Indexed, PydanticObjectId
from datetime import datetime
from typing import Optional


class Book(Document):
    """Book document schema for uploaded books."""
    book_title: str
    book_author: Optional[str] = None
    file_url: str  # S3 URL or local file path
    file_type: str  # pdf, txt, epub
    file_size: int  # Size in bytes
    uploaded_by: Indexed(PydanticObjectId)  # User ID reference
    child_age: int  # For age-appropriate filtering
    is_indexed: bool = False  # Whether content is indexed in ChromaDB
    upload_date: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "books"
        indexes = [
            "uploaded_by",
            ("uploaded_by", "upload_date"),  # Compound index for user's books sorted by date
            "book_title",
            "child_age",
        ]
