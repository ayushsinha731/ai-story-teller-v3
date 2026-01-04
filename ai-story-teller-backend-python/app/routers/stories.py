"""Story management routes."""
from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from bson import ObjectId
from app.models.story import CreateStoryRequest, StoryResponse
from app.models.assignment import AssignmentResponse
from app.models.feedback import FeedbackRequest, FeedbackResponse
from app.services.story_service import story_service
from app.middleware.auth import get_current_user
from app.schemas.user import User
from app.schemas.story import Story
from app.schemas.assignment import Assignment
from app.schemas.feedback import Feedback
from app.exceptions import NotFoundError, ForbiddenError
from app.utils.logger import logger

router = APIRouter(prefix="/api/story", tags=["stories"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_story(
    story_data: CreateStoryRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new story with RAG-enhanced generation.
    Protected route.
    """
    try:
        story = await story_service.create_story(
            story_data=story_data,
            user_id=current_user.id,
            author_name=current_user.parent_name
        )
        
        # Serialize story with proper field names
        story_dict = story.model_dump(by_alias=True)
        story_dict["id"] = str(story.id)  # Add id field for frontend
        
        return {
            "message": "Story created successfully",
            "story": story_dict
        }
    except Exception as e:
        logger.error(f"Error creating story: {e}")
        raise


@router.get("/getStory/{sid}")
async def get_story(
    sid: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a single story by ID.
    Protected route - only returns story if user owns it.
    """
    try:
        story = await story_service.get_story(sid, current_user.id)
        
        # Serialize story with proper field names
        story_dict = {
            "id": str(story.id),
            "storyTitle": story.story_title,
            "storyDescription": story.story_description,
            "storyContent": [
                {
                    "pageText": page.page_text,
                    "pageImage": page.page_image
                }
                for page in story.story_content
            ],
            "storyAuthor": story.story_author,
            "createdBy": str(story.created_by),
            "maxPages": story.max_pages,
            "createdAt": story.created_at.isoformat(),
            "updatedAt": story.updated_at.isoformat()
        }
        
        return {"story": story_dict}
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        logger.error(f"Error getting story: {e}")
        raise


@router.get("/stories/{uid}")
async def get_all_stories(
    uid: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get all stories for a user with pagination.
    Public route (no auth required for now - matches original behavior).
    """
    try:
        if not ObjectId.is_valid(uid):
            raise NotFoundError("Invalid user ID format")
        
        stories, total = await story_service.get_all_stories(
            user_id=ObjectId(uid),
            page=page,
            limit=limit
        )
        
        # Serialize stories with proper field names for frontend
        serialized_stories = []
        for story in stories:
            story_dict = {
                "id": str(story.id),
                "storyTitle": story.story_title,
                "storyDescription": story.story_description,
                "storyContent": [
                    {
                        "pageText": page.page_text,
                        "pageImage": page.page_image
                    }
                    for page in story.story_content
                ],
                "storyAuthor": story.story_author,
                "createdBy": str(story.created_by),
                "maxPages": story.max_pages,
                "createdAt": story.created_at.isoformat(),
                "updatedAt": story.updated_at.isoformat()
            }
            serialized_stories.append(story_dict)
        
        return {
            "stories": serialized_stories,
            "total": total,
            "page": page,
            "limit": limit
        }
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error getting all stories: {e}")
        raise


@router.get("/getQuestions/{sid}")
async def get_questions(
    sid: str,
    current_user: User = Depends(get_current_user)
):
    """
    Create or get existing assignment (questions) for a story.
    Protected route.
    """
    try:
        assignment = await story_service.create_assignment(sid, current_user.id)
        
        # Manually serialize to convert ObjectIds to strings
        return {
            "id": str(assignment.id),
            "sid": str(assignment.sid),
            "uid": str(assignment.uid),
            "questions": [
                {
                    "question": q.question,
                    "answer": q.answer,
                    "userAnswer": q.user_answer
                }
                for q in assignment.questions
            ]
        }
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error getting questions: {e}")
        raise


@router.post("/feedback/{sid}", status_code=status.HTTP_200_OK)
async def submit_feedback(
    sid: str,
    feedback_data: FeedbackRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Submit answers and generate feedback.
    Protected route.
    """
    try:
        feedback = await story_service.generate_feedback_for_assignment(
            story_id=sid,
            user_id=current_user.id,
            answers=feedback_data.answers
        )
        
        # Manually serialize to convert ObjectIds to strings
        return {
            "saveFeedbacks": {
                "id": str(feedback.id),
                "sid": str(feedback.sid),
                "uid": str(feedback.uid),
                "feedbacks": feedback.feedbacks
            }
        }
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise


@router.get("/getFeedback/{sid}")
async def get_feedback(
    sid: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get feedback results for a story.
    Protected route.
    """
    try:
        # Note: Original code queries Feedback, but get_feedback method uses Assignment
        # Fixing to query Feedback collection correctly
        feedback = await Feedback.find_one(
            Feedback.sid == ObjectId(sid),
            Feedback.uid == current_user.id
        )
        if not feedback:
            raise NotFoundError("Feedback not found")
        
        return {"feedback": feedback}
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error getting feedback: {e}")
        raise


@router.get("/getFullStory/{sid}")
async def get_full_story(
    sid: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get full story text (combined from all pages).
    Protected route.
    """
    try:
        story = await story_service.get_story(sid, current_user.id)
        whole_story = " ".join([page.page_text for page in story.story_content])
        
        return {"wholeStory": whole_story}
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        logger.error(f"Error getting full story: {e}")
        raise

