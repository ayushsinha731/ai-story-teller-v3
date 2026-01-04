import pytest
from app.services.audio_service import AudioService
from app.schemas.story import Story
from app.schemas.audio import Audio
from app.schemas.user import User
from bson import ObjectId
from unittest.mock import patch, MagicMock

# Unit Tests for Logic
def test_analyze_punctuation():
    """Test punctuation analysis logic."""
    transcript = "Hello world."
    story = "Hello, world!"
    
    diffs = AudioService.analyze_punctuation(transcript, story)
    
    assert len(diffs) > 0
    # Both sentences are index 0
    assert diffs[0]['sentence_index'] == 0
    # Check simple comparison
    assert '.' in diffs[0]['transcript_punctuation']
    assert ',' in diffs[0]['story_punctuation']

def test_highlight_differences():
    """Test difference highlighting logic."""
    original = "Hello world"
    reading = "Hello universe"
    
    html = AudioService.highlight_differences(original, reading)
    
    # Should contain red span for 'world' and green for 'universe'
    assert "text-red-700" in html
    assert "world" in html
    assert "text-green-700" in html
    assert "universe" in html


# Integration Tests
@pytest.mark.asyncio
async def test_upload_audio(client, auth_headers, mock_s3_client):
    """Test audio upload endpoint."""
    # Create a story first
    user = await User.find_one(User.parent_email == "auth_test@example.com")
    story = Story(
        story_title="Audio Test Story",
        story_content=[],
        max_pages=1,
        user_id=user.id
    )
    await story.insert()
    
    # File to upload
    files = {'audio': ('test.mp3', b'filecontent', 'audio/mpeg')}
    
    response = client.post(f"/api/audio/upload/{story.id}", files=files, cookies=auth_headers)
    
    assert response.status_code == 200 # Original code returns 200/201
    audio_id = response.json()
    assert audio_id is not None
    
    # Verify in DB
    audio = await Audio.get(audio_id)
    assert audio is not None
    assert audio.file_name == "test.mp3"


@pytest.mark.asyncio
async def test_process_audio(client, auth_headers, mock_s3_client):
    """Test audio processing endpoint with mocked AI services."""
    # Setup data
    user = await User.find_one(User.parent_email == "auth_test@example.com")
    story = Story(
        story_title="Process Story",
        story_content=[],
        max_pages=1,
        user_id=user.id
    )
    await story.insert()
    
    # Create audio record directly
    audio = Audio(
        file_path="http://mock/audio.mp3",
        file_name="audio.mp3",
        whole_story="The quick brown fox.",
        sid=story.id,
        user_id=user.id
    )
    await audio.insert()
    
    # Mock AudioService helper methods to avoid real API calls
    with patch.object(AudioService, 'transcribe_audio', return_value="The quick red fox.") as mock_transcribe, \
         patch.object(AudioService, 'enhance_transcript', return_value="The quick brown fox.") as mock_enhance:
         
        response = client.get(f"/api/audio/process-audio/{audio.id}", cookies=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "transcript" in data
        assert "score" in data
        assert "punctuation_analysis" in data
        assert "highlighted_diff" in data
        
        # Verify logic called
        # "red" vs "brown" should cause a difference
        assert data["transcript"] == "The quick red fox."
