import os
import pytest
import asyncio
from typing import Generator
from unittest.mock import MagicMock, patch

# Mock environment variables before importing anything else
os.environ["MONGODB_URI"] = "mongodb://mock"
os.environ["DATABASE_NAME"] = "test_db"
os.environ["JWT_SECRET"] = "test_secret"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["OPENAI_API_KEY"] = "sk-test"
os.environ["ASSEMBLY_AI_API_KEY"] = "test_key"
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["S3_BUCKET_NAME"] = "test-bucket"
os.environ["LOG_LEVEL"] = "INFO"

from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from beanie import init_beanie

from app.main import app
from app.database import connect_db
from app.schemas.user import User
from app.schemas.story import Story
from app.schemas.assignment import Assignment
from app.schemas.feedback import Feedback
from app.schemas.audio import Audio


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def mock_db():
    """Initialize Beanie with a mock MongoDB client."""
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client.test_db,
        document_models=[User, Story, Assignment, Feedback, Audio]
    )
    yield
    # Clean up - drop database not needed with mock client usually, but good practice
    # client.drop_database("test_db")


@pytest.fixture(scope="function")
async def client(mock_db) -> Generator:
    """Create a FastAPI TestClient with mocked dependencies."""
    # Override startup event to prevent real DB connection
    with patch("app.main.connect_db", return_value=None):
        with TestClient(app) as c:
            yield c


@pytest.fixture
def mock_s3_client():
    """Mock the S3 client wrapper."""
    with patch("app.utils.s3_client.s3_client") as mock:
        mock.upload_audio.return_value = ("test-key", "https://s3.amazonaws.com/test-bucket/test.mp3")
        yield mock


@pytest.fixture
def mock_openai():
    """Mock OpenAI interactions."""
    with patch("app.services.rag_service.OpenAIEmbeddings"), \
         patch("app.services.rag_service.Chroma"), \
         patch("app.openai_client.story_generator.AsyncOpenAI"), \
         patch("app.services.audio_service.openai_client"):
        yield


@pytest.fixture
async def auth_headers(client):
    """Create a user and return auth headers/cookies."""
    # Create test user directly in DB
    user = User(
        parent_name="Test Parent",
        parent_email="test@example.com",
        child_name="Test Child",
        child_age=10,
        password="hashed_password_placeholder",  # In real auth, this would be hashed
        child_standard=5
    )
    # We need to manually insert because the signup route hashes the password
    # For integration testing login, we might want to use the signup endpoint instead
    # But for just getting a token, we can mock the token creation or login flow
    
    # Let's use the signup endpoint to create a valid user with hashed password
    response = client.post("/api/user/signup", json={
        "parent_name": "Test Parent",
        "parent_email": "auth_test@example.com",
        "child_name": "Test Child",
        "child_age": 10,
        "password": "Password123!",
        "child_standard": 5
    })
    
    # The response should have set the cookie
    assert response.status_code == 201
    return response.cookies
