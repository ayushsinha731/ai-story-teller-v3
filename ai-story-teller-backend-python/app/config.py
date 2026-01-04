"""Application configuration with environment variable validation."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB
    mongodb_uri: str
    database_name: str = "test"
    
    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_days: int = 15
    
    # OpenAI
    openai_api_key: str
    
    # AssemblyAI
    assembly_ai_api_key: str
    
    # AWS S3
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    s3_bucket_name: str
    
    # Server URLs
    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8000"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost", "http://localhost:80"]
    
    # Logging
    log_level: str = "INFO"
    
    # ChromaDB
    chroma_db_path: str = "./chroma_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

