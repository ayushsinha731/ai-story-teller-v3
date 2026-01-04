"""Audio upload and processing routes."""
from fastapi import APIRouter, Depends, UploadFile, File, status
from app.services.audio_service import audio_service
from app.middleware.auth import get_current_user
from app.schemas.user import User
from app.exceptions import NotFoundError
from app.utils.logger import logger

router = APIRouter(tags=["audio"])


@router.post("/upload/{sid}", status_code=status.HTTP_201_CREATED)
async def upload_audio(
    sid: str,
    audio: UploadFile = File(..., description="Audio file to upload"),
    current_user: User = Depends(get_current_user)
):
    """
    Upload audio file to S3.
    Protected route.
    """
    try:
        # Read audio file content
        audio_content = await audio.read()
        
        # Upload to S3 and create audio record
        audio_doc = await audio_service.upload_audio_to_s3(
            audio_file=audio_content,
            file_name=audio.filename,
            story_id=sid
        )
        
        return str(audio_doc.id)
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error uploading audio: {e}")
        raise


@router.get("/audio/finalFeedback/{aid}")
async def get_audio_feedback(
    aid: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get audio feedback with story data.
    Protected route.
    """
    try:
        result = await audio_service.get_audio_feedback(aid)
        
        # Convert to response format
        audio_doc = result["audio"]
        story_doc = result["story"]
        
        return {
            "audio": {
                "id": str(audio_doc.id),
                "filePath": audio_doc.file_path,
                "fileName": audio_doc.file_name,
                "transcript": audio_doc.transcript,
                "score": audio_doc.score,
                "wholeStory": audio_doc.whole_story,
                "sid": str(audio_doc.sid) if audio_doc.sid else None,
                "createdAt": audio_doc.created_at
            },
            "story": {
                "id": str(story_doc.id),
                "storyTitle": story_doc.story_title,
                "storyDescription": story_doc.story_description,
                "storyContent": [
                    {
                        "pageText": page.page_text,
                        "pageImage": page.page_image
                    }
                    for page in story_doc.story_content
                ],
                "storyAuthor": story_doc.story_author,
                "maxPages": story_doc.max_pages
            } if story_doc else None
        }
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error getting audio feedback: {e}")
        raise


@router.get("/process-audio/{aid}")
async def process_audio(
    aid: str,
    current_user: User = Depends(get_current_user)
):
    """
    Process audio: transcribe, enhance, and calculate score.
    Protected route.
    """
    try:
        result = await audio_service.process_audio(aid)
        return result
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise

