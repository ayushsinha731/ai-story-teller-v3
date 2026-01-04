"""Database connection and initialization."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.schemas.user import User
from app.schemas.story import Story
from app.schemas.assignment import Assignment
from app.schemas.feedback import Feedback
from app.schemas.audio import Audio
from app.schemas.book import Book
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager."""
    client: AsyncIOMotorClient = None


database = Database()


async def connect_db() -> None:
    """Create database connection and initialize Beanie."""
    try:
        database.client = AsyncIOMotorClient(settings.mongodb_uri)
        await init_beanie(
            database=database.client[settings.database_name],
            document_models=[User, Story, Assignment, Feedback, Audio, Book]
        )
        logger.info(f"✅ Database connected to {settings.database_name}")
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        raise


async def close_db() -> None:
    """Close database connection."""
    if database.client:
        database.client.close()
        logger.info("❌ Database disconnected")

