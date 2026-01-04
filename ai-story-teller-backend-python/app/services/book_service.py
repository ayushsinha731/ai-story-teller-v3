"""Book service for file upload, processing, and indexing."""
import io
import os
import uuid
from typing import Optional, Tuple
from fastapi import UploadFile
import boto3
from botocore.exceptions import ClientError
from PyPDF2 import PdfReader
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from app.config import settings
from app.schemas.book import Book
from app.models.book import BookResponse, UploadBookMetadata
from app.services.rag_service import rag_service
from app.utils.logger import logger
from bson import ObjectId


# File upload constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.epub'}


class BookService:
    """Service for managing book uploads and processing."""
    
    def __init__(self):
        """Initialize S3 client."""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.s3_bucket_name
    
    def _validate_file(self, file: UploadFile) -> None:
        """
        Validate uploaded file.
        
        Args:
            file: Uploaded file
            
        Raises:
            ValueError: If file is invalid
        """
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
    
    async def _upload_to_s3(self, file: UploadFile, object_key: str) -> str:
        """
        Upload file to S3.
        
        Args:
            file: File to upload
            object_key: S3 object key
            
        Returns:
            S3 URL of uploaded file
        """
        try:
            # Read file content
            file_content = await file.read()
            
            # Check file size
            if len(file_content) > MAX_FILE_SIZE:
                raise ValueError(f"File size exceeds {MAX_FILE_SIZE / (1024*1024)}MB limit")
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=file.content_type or 'application/octet-stream'
            )
            
            # Generate URL
            file_url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{object_key}"
            
            # Reset file pointer for text extraction
            await file.seek(0)
            
            return file_url, len(file_content)
            
        except ClientError as e:
            logger.error(f"S3 upload error: {e}")
            raise Exception(f"Failed to upload file to S3: {str(e)}")
    
    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PdfReader(pdf_file)
            
            text_parts = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"PDF text extraction error: {e}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_text_from_epub(self, file_content: bytes) -> str:
        """Extract text from EPUB file."""
        try:
            book = epub.read_epub(io.BytesIO(file_content))
            
            text_parts = []
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content()
                    soup = BeautifulSoup(content, 'html.parser')
                    text = soup.get_text()
                    if text.strip():
                        text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"EPUB text extraction error: {e}")
            raise Exception(f"Failed to extract text from EPUB: {str(e)}")
    
    def _extract_text_from_txt(self, file_content: bytes) -> str:
        """Extract text from TXT file."""
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return file_content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            # If all fail, use utf-8 with error handling
            return file_content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"TXT text extraction error: {e}")
            raise Exception(f"Failed to extract text from TXT: {str(e)}")
    
    async def extract_text(self, file: UploadFile, file_type: str) -> str:
        """
        Extract text content from uploaded file.
        
        Args:
            file: Uploaded file
            file_type: File extension
            
        Returns:
            Extracted text content
        """
        file_content = await file.read()
        
        if file_type == '.pdf':
            text = self._extract_text_from_pdf(file_content)
        elif file_type == '.epub':
            text = self._extract_text_from_epub(file_content)
        elif file_type == '.txt':
            text = self._extract_text_from_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Reset file pointer
        await file.seek(0)
        
        return text.strip()
    
    async def upload_book(
        self,
        file: UploadFile,
        user_id: str,
        child_age: int,
        metadata: Optional[UploadBookMetadata] = None
    ) -> BookResponse:
        """
        Upload and process a book file.
        
        Args:
            file: Uploaded file
            user_id: User ID
            child_age: Child's age
            metadata: Optional book metadata
            
        Returns:
            Created book response
        """
        try:
            # Validate file
            self._validate_file(file)
            
            # Get file extension
            file_type = os.path.splitext(file.filename)[1].lower()
            
            # Generate unique object key
            unique_id = str(uuid.uuid4())
            object_key = f"books/{user_id}/{unique_id}{file_type}"
            
            # Upload to S3
            file_url, file_size = await self._upload_to_s3(file, object_key)
            
            # Extract text content
            logger.info(f"Extracting text from {file.filename}")
            text_content = await self.extract_text(file, file_type)
            
            if not text_content:
                raise ValueError("No text content could be extracted from the file")
            
            # Determine book title
            book_title = metadata.book_title if metadata and metadata.book_title else file.filename
            book_author = metadata.book_author if metadata else None
            
            # Create book document
            book = Book(
                book_title=book_title,
                book_author=book_author,
                file_url=file_url,
                file_type=file_type.replace('.', ''),
                file_size=file_size,
                uploaded_by=ObjectId(user_id),
                child_age=child_age,
                is_indexed=False
            )
            
            await book.insert()
            
            # Index in ChromaDB asynchronously
            try:
                logger.info(f"Indexing book {book.id} in vector database")
                await rag_service.add_book_to_index(
                    book_id=str(book.id),
                    book_title=book_title,
                    book_author=book_author,
                    book_content=text_content,
                    user_id=user_id,
                    child_age=child_age
                )
                
                # Update indexing status
                book.is_indexed = True
                await book.save()
                
            except Exception as e:
                logger.error(f"Failed to index book in vector DB: {e}")
                # Don't fail the upload, just log the error
            
            logger.info(f"Book uploaded successfully: {book.id}")
            
            return BookResponse(
                id=str(book.id),
                book_title=book.book_title,
                book_author=book.book_author,
                file_url=book.file_url,
                file_type=book.file_type,
                file_size=book.file_size,
                uploaded_by=str(book.uploaded_by),
                child_age=book.child_age,
                is_indexed=book.is_indexed,
                upload_date=book.upload_date,
                updated_at=book.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error uploading book: {e}")
            raise
    
    async def get_user_books(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[list[BookResponse], int]:
        """
        Get all books for a user.
        
        Args:
            user_id: User ID
            page: Page number
            limit: Items per page
            
        Returns:
            Tuple of (books list, total count)
        """
        try:
            user_object_id = ObjectId(user_id)
            
            # Get total count
            total = await Book.find(Book.uploaded_by == user_object_id).count()
            
            # Get paginated books
            skip = (page - 1) * limit
            books = await Book.find(
                Book.uploaded_by == user_object_id
            ).sort(-Book.upload_date).skip(skip).limit(limit).to_list()
            
            # Convert to response models
            book_responses = [
                BookResponse(
                    id=str(book.id),
                    book_title=book.book_title,
                    book_author=book.book_author,
                    file_url=book.file_url,
                    file_type=book.file_type,
                    file_size=book.file_size,
                    uploaded_by=str(book.uploaded_by),
                    child_age=book.child_age,
                    is_indexed=book.is_indexed,
                    upload_date=book.upload_date,
                    updated_at=book.updated_at
                )
                for book in books
            ]
            
            return book_responses, total
            
        except Exception as e:
            logger.error(f"Error getting user books: {e}")
            raise
    
    async def delete_book(self, book_id: str, user_id: str) -> None:
        """
        Delete a book.
        
        Args:
            book_id: Book ID
            user_id: User ID (for authorization)
            
        Raises:
            ValueError: If book not found or unauthorized
        """
        try:
            book = await Book.get(book_id)
            
            if not book:
                raise ValueError("Book not found")
            
            if str(book.uploaded_by) != user_id:
                raise ValueError("Unauthorized to delete this book")
            
            # Delete from S3
            try:
                # Extract object key from URL
                # URL format: https://bucket.s3.region.amazonaws.com/key
                url_parts = book.file_url.split('.amazonaws.com/')
                if len(url_parts) > 1:
                    object_key = url_parts[1]
                    self.s3_client.delete_object(
                        Bucket=self.bucket_name,
                        Key=object_key
                    )
            except Exception as e:
                logger.warning(f"Failed to delete from S3: {e}")
            
            # Delete from database
            await book.delete()
            
            logger.info(f"Book deleted: {book_id}")
            
            # Note: ChromaDB doesn't have easy deletion by metadata
            # The old chunks will remain but won't match user_id queries
            
        except Exception as e:
            logger.error(f"Error deleting book: {e}")
            raise


# Singleton instance
book_service = BookService()
