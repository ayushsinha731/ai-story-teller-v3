"""FastAPI application main entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import connect_db, close_db
from app.routers import users, stories, audio, books
from app.middleware.error_handler import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.exceptions import AppException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.logger import logger
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting application...")
    await connect_db()
    yield
    # Shutdown
    logger.info("Shutting down application...")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title="AI Storyteller API",
    description="AI-powered storytelling platform with RAG enhancement",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"Loaded CORS origins: {settings.cors_origins}")

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(users.router)
app.include_router(stories.router)
app.include_router(audio.router)
app.include_router(books.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World! AI Storyteller API is running."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

