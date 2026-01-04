"""User document model."""
from beanie import Document, Indexed
from datetime import datetime
from typing import Optional


class User(Document):
    """User document schema."""
    parent_name: str
    parent_email: Indexed(str, unique=True)
    child_name: str
    child_age: int
    password: str
    child_standard: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "users"
        indexes = [
            "parent_email",  # Already indexed via Indexed
            "child_age",
        ]

