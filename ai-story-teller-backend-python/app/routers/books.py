"""Book upload and management routes."""
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, status, HTTPException
from typing import Optional
from bson import ObjectId

from app.models.book import BookResponse, BookListResponse, UploadBookMetadata
from app.services.book_service import book_service
from app.middleware.auth import get_current_user
from app.schemas.user import User
from app.utils.logger import logger

router = APIRouter(prefix="/api/books", tags=["books"])


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
async def upload_book(
    file: UploadFile = File(..., description="Book file (PDF, TXT, or EPUB)"),
    book_title: Optional[str] = Form(None, description="Book title (optional)"),
    book_author: Optional[str] = Form(None, description="Book author (optional)"),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new book file.
    Protected route.
    
    Args:
        file: Book file to upload
        book_title: Optional book title
        book_author: Optional book author
        current_user: Authenticated user
        
    Returns:
        Created book response
    """
    try:
        # Create metadata if provided
        metadata = None
        if book_title or book_author:
            metadata = UploadBookMetadata(
                book_title=book_title,
                book_author=book_author
            )
        
        book = await book_service.upload_book(
            file=file,
            user_id=str(current_user.id),
            child_age=current_user.child_age,
            metadata=metadata
        )
        
        logger.info(f"Book uploaded by user {current_user.id}: {book.id}")
        return book
        
    except ValueError as e:
        logger.warning(f"Invalid book upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading book: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload book")


@router.get("", response_model=BookListResponse)
async def get_user_books(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user)
):
    """
    Get all books for the authenticated user.
    Protected route.
    
    Args:
        page: Page number
        limit: Items per page
        current_user: Authenticated user
        
    Returns:
        List of user's books with pagination
    """
    try:
        books, total = await book_service.get_user_books(
            user_id=str(current_user.id),
            page=page,
            limit=limit
        )
        
        return BookListResponse(
            books=books,
            total=total,
            page=page,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting books: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve books")


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(
    book_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a book.
    Protected route - only owner can delete.
    
    Args:
        book_id: Book ID to delete
        current_user: Authenticated user
        
    Returns:
        Success message
    """
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(status_code=400, detail="Invalid book ID")
        
        await book_service.delete_book(
            book_id=book_id,
            user_id=str(current_user.id)
        )
        
        return {"message": "Book deleted successfully"}
        
    except ValueError as e:
        logger.warning(f"Invalid book deletion: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting book: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete book")
