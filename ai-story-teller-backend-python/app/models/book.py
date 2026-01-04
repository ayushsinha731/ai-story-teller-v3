"""Pydantic models for book requests and responses."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UploadBookMetadata(BaseModel):
    """Optional metadata for book upload."""
    book_title: Optional[str] = Field(None, max_length=200, description="Book title", alias="bookTitle")
    book_author: Optional[str] = Field(None, max_length=100, description="Book author", alias="bookAuthor")
    
    model_config = ConfigDict(populate_by_name=True)


class BookResponse(BaseModel):
    """Book response model."""
    id: str
    book_title: str = Field(..., serialization_alias="bookTitle")
    book_author: Optional[str] = Field(None, serialization_alias="bookAuthor")
    file_url: str = Field(..., serialization_alias="fileUrl")
    file_type: str = Field(..., serialization_alias="fileType")
    file_size: int = Field(..., serialization_alias="fileSize")
    uploaded_by: str = Field(..., serialization_alias="uploadedBy")
    child_age: int = Field(..., serialization_alias="childAge")
    is_indexed: bool = Field(..., serialization_alias="isIndexed")
    upload_date: datetime = Field(..., serialization_alias="uploadDate")
    updated_at: datetime = Field(..., serialization_alias="updatedAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class BookListResponse(BaseModel):
    """Response model for paginated book list."""
    books: list[BookResponse]
    total: int
    page: int
    limit: int
