"""Pydantic models for story requests and responses."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class PageContent(BaseModel):
    """Page content model."""
    page_text: str = Field(..., alias="pageText")
    page_image: Optional[str] = Field(None, alias="pageImage")


class CreateStoryRequest(BaseModel):
    """Create story request model."""
    story_title: str = Field(..., min_length=1, max_length=200, description="Story title", alias="storyTitle")
    story_description: str = Field(..., min_length=10, max_length=1000, description="Story description", alias="storyDescription")
    max_pages: int = Field(..., ge=1, le=20, description="Maximum number of pages (1-20)", alias="maxPages")
    include_image: bool = Field(default=False, description="Whether to include images", alias="includeImage")
    child_age: int = Field(..., ge=5, le=15, description="Child's age for age-appropriate content", alias="childAge")
    use_books_context: bool = Field(default=False, description="Use user's uploaded books for context", alias="useBooksContext")
    use_history_context: bool = Field(default=False, description="Use user's reading history (past stories) for context", alias="useHistoryContext")
    
    model_config = ConfigDict(populate_by_name=True)


class StoryResponse(BaseModel):
    """Story response model."""
    id: str
    story_title: str = Field(..., alias="storyTitle")
    story_description: str = Field(..., alias="storyDescription")
    story_content: List[PageContent] = Field(..., alias="storyContent")
    story_author: str = Field(..., alias="storyAuthor")
    created_by: str = Field(..., alias="createdBy")
    max_pages: int = Field(..., alias="maxPages")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

