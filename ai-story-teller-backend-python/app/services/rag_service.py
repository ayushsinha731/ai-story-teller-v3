"""RAG (Retrieval-Augmented Generation) service using ChromaDB."""
from typing import List, Dict, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from app.config import settings
from app.utils.logger import logger


class RAGService:
    """RAG service for story retrieval and context enhancement."""
    
    def __init__(self):
        """Initialize RAG service with embeddings and vector store."""
        try:
            # Initialize OpenAI embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=settings.openai_api_key
            )
            
            # Initialize ChromaDB vector store
            os.makedirs(settings.chroma_db_path, exist_ok=True)
            self.vector_store = Chroma(
                persist_directory=settings.chroma_db_path,
                embedding_function=self.embeddings
            )
            
            # Text splitter for chunking stories
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            logger.info("RAG service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing RAG service: {e}")
            raise
    
    async def add_story_to_index(
        self,
        story_id: str,
        story_title: str,
        story_description: str,
        story_content: str,
        child_age: int,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Index a story for RAG retrieval.
        
        Args:
            story_id: Unique story identifier
            story_title: Story title
            story_description: Story description
            story_content: Full story content text
            child_age: Child's age for filtering
            metadata: Additional metadata to store
        """
        try:
            # Combine story content
            full_text = f"Title: {story_title}\n\nDescription: {story_description}\n\nContent: {story_content}"
            
            # Split into chunks
            chunks = self.text_splitter.split_text(full_text)
            
            # Create documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = {
                    "story_id": story_id,
                    "story_title": story_title,
                    "child_age": child_age,
                    "chunk_index": i,
                    "type": "story"
                }
                if metadata:
                    doc_metadata.update(metadata)
                
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata=doc_metadata
                    )
                )
            
            # Add to vector store
            self.vector_store.add_documents(documents)

            
            logger.info(f"Story indexed: {story_id} ({len(chunks)} chunks)")
        except Exception as e:
            logger.error(f"Error indexing story: {e}")
            raise
    
    async def add_book_to_index(
        self,
        book_id: str,
        book_title: str,
        book_author: Optional[str],
        book_content: str,
        user_id: str,
        child_age: int,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Index a book for RAG retrieval.
        
        Args:
            book_id: Unique book identifier
            book_title: Book title
            book_author: Book author (optional)
            book_content: Full book text content
            user_id: User ID who uploaded the book
            child_age: Child's age for filtering
            metadata: Additional metadata to store
        """
        try:
            # Combine book content
            author_text = f"Author: {book_author}\n\n" if book_author else ""
            full_text = f"Title: {book_title}\n\n{author_text}Content: {book_content}"
            
            # Split into chunks
            chunks = self.text_splitter.split_text(full_text)
            
            # Create documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = {
                    "book_id": book_id,
                    "book_title": book_title,
                    "user_id": user_id,
                    "child_age": child_age,
                    "chunk_index": i,
                    "type": "book"
                }
                if book_author:
                    doc_metadata["book_author"] = book_author
                if metadata:
                    doc_metadata.update(metadata)
                
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata=doc_metadata
                    )
                )
            
            # Add to vector store
            self.vector_store.add_documents(documents)

            
            logger.info(f"Book indexed: {book_id} ({len(chunks)} chunks)")
        except Exception as e:
            logger.error(f"Error indexing book: {e}")
            raise

    
    async def retrieve_similar_stories(
        self,
        query: str,
        child_age: int,
        top_k: int = 3,
        filters: Optional[Dict] = None
    ) -> List[Document]:
        """
        Retrieve similar stories based on semantic search.
        
        Args:
            query: Search query string
            child_age: Child's age for filtering
            top_k: Number of results to return
            filters: Additional filters
            
        Returns:
            List of similar story documents
        """
        try:
            # Build metadata filter
            search_filters = {"child_age": child_age, "type": "story"}
            if filters:
                search_filters.update(filters)
            
            # Perform similarity search
            # Note: ChromaDB filter syntax may vary - adjust as needed
            results = self.vector_store.similarity_search(
                query,
                k=top_k
            )
            
            # Filter by metadata (ChromaDB may handle this differently)
            # For now, filter results manually
            filtered_results = [
                doc for doc in results
                if doc.metadata.get("child_age") == child_age
                and doc.metadata.get("type") == "story"
            ]
            
            logger.info(f"Retrieved {len(filtered_results)} similar stories for query")
            return filtered_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error retrieving similar stories: {e}")
            return []
    
    async def retrieve_educational_context(
        self,
        topic: str,
        age_group: int,
        top_k: int = 2
    ) -> List[Document]:
        """
        Retrieve educational content for story generation.
        
        Args:
            topic: Topic or theme
            age_group: Child's age group
            top_k: Number of results
            
        Returns:
            List of educational content documents
        """
        try:
            query = f"Educational content for {age_group} year old about {topic}"
            results = self.vector_store.similarity_search(
                query,
                k=top_k
            )
            
            # Filter by type if educational content is indexed
            educational_results = [
                doc for doc in results
                if doc.metadata.get("type") == "educational_content"
            ]
            
            return educational_results[:top_k]
        except Exception as e:
            logger.warning(f"Error retrieving educational context: {e}")
            return []
    
    async def retrieve_from_user_library(
        self,
        query: str,
        user_id: str,
        child_age: int,
        top_k: int = 5,
        include_books: bool = True,
        include_stories: bool = True
    ) -> List[Document]:
        """
        Retrieve content from user's personal library (books and stories).
        
        Args:
            query: Search query string
            user_id: User ID to filter by
            child_age: Child's age for filtering
            top_k: Number of results to return
            include_books: Whether to include books in results
            include_stories: Whether to include stories in results
            
        Returns:
            List of documents from user's library
        """
        try:
            # Perform similarity search with larger k to allow filtering
            results = self.vector_store.similarity_search(
                query,
                k=top_k * 3  # Get more results to filter
            )
            
            # Filter by user_id and type
            filtered_results = []
            for doc in results:
                metadata = doc.metadata
                
                # Check user ownership
                if metadata.get("user_id") != user_id:
                    continue
                
                # Check age appropriateness
                if metadata.get("child_age") != child_age:
                    continue
                
                # Check type filter
                doc_type = metadata.get("type")
                if doc_type == "book" and not include_books:
                    continue
                if doc_type == "story" and not include_stories:
                    continue
                
                filtered_results.append(doc)
                
                if len(filtered_results) >= top_k:
                    break
            
            logger.info(f"Retrieved {len(filtered_results)} documents from user library")
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error retrieving from user library: {e}")
            return []



# Singleton instance
rag_service = RAGService()

