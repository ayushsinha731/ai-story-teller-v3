import pytest
from app.services.rag_service import RAGService
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_add_story_to_index(mock_openai):
    """Test indexing a story."""
    # Mock the vector store specifically for this test if needed, 
    # but mock_openai fixture already patches 'app.services.rag_service.Chroma'
    
    # We need to instantiate the service inside the test or use a fixture if we want a fresh one
    # The global 'rag_service' in app.services.rag_service is instantiated at module level.
    # It might have been instantiated before our mocks if imported earlier.
    # To be safe, let's patch the class and instantiate a new instance or patch the methods.
    
    with patch("app.services.rag_service.RAGService.add_story_to_index") as mock_add:
        from app.services.rag_service import rag_service
        
        await rag_service.add_story_to_index(
            story_id="test_id",
            story_title="Title",
            story_description="Desc",
            story_content="Content",
            child_age=5
        )
        
        mock_add.assert_called_once()

@pytest.mark.asyncio
async def test_retrieve_similar_stories(mock_openai):
    """Test retrieval logic."""
    # We want to test the wrapping logic, not the vector store itself (which is external)
    
    with patch("app.services.rag_service.RAGService.retrieve_similar_stories", return_value=[]) as mock_retrieve:
        from app.services.rag_service import rag_service
        
        results = await rag_service.retrieve_similar_stories("query", child_age=5)
        
        assert results == []
        mock_retrieve.assert_called_with("query", child_age=5)
