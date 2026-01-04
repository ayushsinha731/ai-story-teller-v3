"""Pydantic models for user requests and responses."""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class UserSignUpRequest(BaseModel):
    """User registration request model."""
    parent_name: str = Field(..., min_length=1, max_length=100, description="Parent's name", alias="parentName")
    parent_email: EmailStr = Field(..., description="Parent's email address", alias="parentEmail")
    child_name: str = Field(..., min_length=1, max_length=100, description="Child's name", alias="childName")
    child_age: int = Field(..., ge=5, le=15, description="Child's age (5-15)", alias="childAge")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    child_standard: str = Field(..., pattern=r'^[1-8]$', description="Child's standard/grade (1-8)", alias="childStandard")
    
    model_config = ConfigDict(populate_by_name=True)


class UserLoginRequest(BaseModel):
    """User login request model."""
    parent_email: EmailStr = Field(..., description="Parent's email address", alias="parentEmail")
    password: str = Field(..., description="Password")
    
    model_config = ConfigDict(populate_by_name=True)


class UserResponse(BaseModel):
    """User response model."""
    user_id: str = Field(..., serialization_alias="userId")
    parent_name: str = Field(..., serialization_alias="parentName")
    parent_email: str = Field(..., serialization_alias="parentEmail")
    child_name: str = Field(..., serialization_alias="childName")
    child_age: int = Field(..., serialization_alias="childAge")
    child_standard: str = Field(..., serialization_alias="childStandard")
    
    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Login response model matching legacy API."""
    user_id: str = Field(..., serialization_alias="userId")
    parent_name: str = Field(..., serialization_alias="parentName")
    parent_email: str = Field(..., serialization_alias="parentEmail")
    child_name: str = Field(..., serialization_alias="childName")
    child_age: int = Field(..., serialization_alias="childAge")
    child_standard: str = Field(..., serialization_alias="childStandard")
    message: str

