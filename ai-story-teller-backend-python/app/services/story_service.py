"""Story service for story management and operations."""
from typing import List, Optional
from bson import ObjectId
from app.schemas.story import Story, PageContent
from app.schemas.assignment import Assignment
from app.schemas.feedback import Feedback
from app.models.story import CreateStoryRequest
from app.agents.story_graph import run_story_generation
from app.openai_client.image_generator import generate_image
from app.openai_client.question_generator import generate_questions
from app.openai_client.feedback_generator import generate_feedback
from app.services.rag_service import rag_service
from app.exceptions import NotFoundError, ForbiddenError
from app.config import settings
from app.utils.logger import logger
import asyncio
import httpx
import uuid
from app.utils.s3_client import s3_client


class StoryService:
    """Service for story-related operations."""
    
    @staticmethod
    async def create_story(
        story_data: CreateStoryRequest,
        user_id: ObjectId,
        author_name: str
    ) -> Story:
        """
        Create a new story with RAG-enhanced generation.
        
        Args:
            story_data: Story creation data
            user_id: ID of user creating the story
            author_name: Name of the author
            
        Returns:
            Created story document
        """
        try:
            # Generate story using OpenAI with RAG
            # Generate story using Story Graph Agent
            generated_story = await run_story_generation(
                story_description=story_data.story_description,
                story_title=story_data.story_title,
                max_pages=story_data.max_pages,
                child_age=story_data.child_age,
                user_id=str(user_id),
                use_books_context=story_data.use_books_context,
                use_history_context=story_data.use_history_context
            )
            
            # Process story content and images
            story_contents = []
            page_texts = generated_story.get("storyContent", [])
            
            # Generate images if requested (parallelize where possible)
            image_tasks = []
            if story_data.include_image:
                for i, page_data in enumerate(page_texts):
                    page_text = page_data.get("pageText", "")
                    # Generate images for pages 0, 2, 4, etc. (every other page)
                    if i % 3 == 0 or i % 3 == 2:
                        image_tasks.append((i, generate_image(
                            page_text=page_text,
                            child_age=story_data.child_age,
                            story_title=story_data.story_title
                        )))
            
            # Execute image generation in parallel
            image_results = {}
            if image_tasks:
                image_coroutines = [task[1] for task in image_tasks]
                image_urls = await asyncio.gather(*image_coroutines, return_exceptions=True)
                for (idx, _), url in zip(image_tasks, image_urls):
                    if not isinstance(url, Exception) and url:
                        image_results[idx] = url
            
            # Build story content with images
            for i, page_data in enumerate(page_texts):
                page_text = page_data.get("pageText", "")
                page_image = None
                
                if i in image_results:
                    # Use OpenAI image URL directly
                    openai_image_url = image_results[i]
                    
                    try:
                        # Download image from OpenAI
                        async with httpx.AsyncClient() as client:
                            response = await client.get(openai_image_url)
                            if response.status_code == 200:
                                image_content = response.content
                                # Upload to S3
                                image_filename = f"{uuid.uuid4()}.png"
                                page_image = await s3_client.upload_image(image_content, image_filename)
                            else:
                                logger.warning(f"Failed to download image from OpenAI: {response.status_code}")
                                page_image = openai_image_url # Fallback
                    except Exception as e:
                        logger.error(f"Error saving image to S3: {e}")
                        page_image = openai_image_url # Fallback
                
                story_contents.append(PageContent(
                    page_text=page_text,
                    page_image=page_image
                ))
            
            # Create story document
            story = Story(
                story_title=story_data.story_title,
                story_description=story_data.story_description,
                story_content=story_contents,
                story_author=author_name,
                created_by=user_id,
                max_pages=story_data.max_pages
            )
            await story.insert()
            
            # Index story in ChromaDB for RAG
            try:
                story_content_text = " ".join([page.page_text for page in story_contents])
                await rag_service.add_story_to_index(
                    story_id=str(story.id),
                    story_title=story.story_title,
                    story_description=story.story_description,
                    story_content=story_content_text,
                    child_age=story_data.child_age,
                    metadata={"user_id": str(user_id), "author": author_name}
                )
            except Exception as e:
                logger.warning(f"Failed to index story in ChromaDB: {e}")
            
            logger.info(f"Story created: {story.id}")
            return story
            
        except Exception as e:
            logger.error(f"Error creating story: {e}")
            raise Exception(f"Failed to create story: {str(e)}")
    
    @staticmethod
    async def get_story(story_id: str, user_id: ObjectId) -> Story:
        """
        Get a story by ID with ownership validation.
        
        Args:
            story_id: Story ID
            user_id: User ID for ownership check
            
        Returns:
            Story document
        """
        try:
            story = await Story.get(story_id)
            if not story:
                raise NotFoundError("Story not found")
            
            if story.created_by != user_id:
                raise ForbiddenError("Unauthorized access to this story")
            
            return story
        except (NotFoundError, ForbiddenError):
            raise
        except Exception as e:
            logger.error(f"Error getting story: {e}")
            raise Exception(f"Failed to get story: {str(e)}")
    
    @staticmethod
    async def get_all_stories(
        user_id: ObjectId,
        page: int = 1,
        limit: int = 10
    ) -> tuple[List[Story], int]:
        """
        Get all stories for a user with pagination.
        
        Args:
            user_id: User ID
            page: Page number (1-based)
            limit: Items per page
            
        Returns:
            Tuple of (stories list, total count)
        """
        try:
            skip = (page - 1) * limit
            stories = await Story.find(
                Story.created_by == user_id
            ).sort(-Story.created_at).skip(skip).limit(limit).to_list()
            
            total = await Story.find(Story.created_by == user_id).count()
            
            return stories, total
        except Exception as e:
            logger.error(f"Error getting all stories: {e}")
            raise Exception(f"Failed to get stories: {str(e)}")
    
    @staticmethod
    async def create_assignment(story_id: str, user_id: ObjectId) -> Assignment:
        """
        Create or get existing assignment for a story.
        
        Args:
            story_id: Story ID
            user_id: User ID
            
        Returns:
            Assignment document
        """
        try:
            # Check if assignment already exists
            existing = await Assignment.find_one(
                Assignment.sid == ObjectId(story_id),
                Assignment.uid == user_id
            )
            if existing:
                return existing
            
            # Get story
            story = await Story.get(story_id)
            if not story:
                raise NotFoundError("Story not found")
            
            # Generate questions
            story_content_dict = [
                {"pageText": page.page_text}
                for page in story.story_content
            ]
            questions_data = await generate_questions(story_content_dict, story.story_title)
            
            # Create assignment
            assignment = Assignment(
                sid=ObjectId(story_id),
                uid=user_id,
                questions=questions_data.get("questions", [])
            )
            await assignment.insert()
            
            logger.info(f"Assignment created: {assignment.id}")
            return assignment
            
        except (NotFoundError, Exception) as e:
            if isinstance(e, NotFoundError):
                raise
            logger.error(f"Error creating assignment: {e}")
            raise Exception(f"Failed to create assignment: {str(e)}")
    
    @staticmethod
    async def generate_feedback_for_assignment(
        story_id: str,
        user_id: ObjectId,
        answers: List[str]
    ) -> Feedback:
        """
        Generate feedback for user answers.
        
        Args:
            story_id: Story ID
            user_id: User ID
            answers: List of user answers
            
        Returns:
            Feedback document
        """
        try:
            # Get assignment
            assignment = await Assignment.find_one(
                Assignment.sid == ObjectId(story_id),
                Assignment.uid == user_id
            )
            if not assignment:
                raise NotFoundError("Assignment not found")
            
            # Get story
            story = await Story.get(story_id)
            if not story:
                raise NotFoundError("Story not found")
            
            # Add user answers to questions
            questions_with_answers = assignment.questions.copy()
            for i, answer in enumerate(answers):
                if i < len(questions_with_answers):
                    questions_with_answers[i].user_answer = answer
            
            # Convert to dict format for feedback generator
            questions_dict = [
                {
                    "question": q.question,
                    "answer": q.answer,
                    "userAnswer": q.user_answer or ""
                }
                for q in questions_with_answers
            ]
            
            story_content_dict = [
                {"pageText": page.page_text}
                for page in story.story_content
            ]
            
            # Generate feedback
            feedback_data = await generate_feedback(questions_dict, story_content_dict)
            
            # Transform camelCase to snake_case for Beanie compatibility
            transformed_feedbacks = []
            for item in feedback_data.get("results", []):
                # Robustly get user answer with multiple key attempts and default
                user_answ = (
                    item.get("userAnswer") or 
                    item.get("user_answer") or 
                    item.get("UserAnswer") or 
                    item.get("userResponse") or 
                    ""
                )
                
                # Robustly get positive reinforcement
                pos_reinf = (
                    item.get("positiveReinforcement") or 
                    item.get("positive_reinforcement") or 
                    item.get("PositiveReinforcement") or 
                    None
                )

                transformed_feedbacks.append({
                    "question": item.get("question", ""),
                    "answer": item.get("answer", ""),
                    "user_answer": user_answ,
                    "rating": item.get("rating", 0),
                    "feedback": item.get("feedback", ""),
                    "positive_reinforcement": pos_reinf
                })
            
            # Create feedback document
            feedback = Feedback(
                sid=ObjectId(story_id),
                uid=user_id,
                feedbacks=transformed_feedbacks
            )
            await feedback.insert()
            
            logger.info(f"Feedback generated: {feedback.id}")
            return feedback
            
        except (NotFoundError, Exception) as e:
            if isinstance(e, NotFoundError):
                raise
            logger.error(f"Error generating feedback: {e}")
            raise Exception(f"Failed to generate feedback: {str(e)}")
    
    @staticmethod
    async def get_feedback(story_id: str, user_id: ObjectId) -> Feedback:
        """
        Get feedback for a story.
        
        Args:
            story_id: Story ID
            user_id: User ID
            
        Returns:
            Feedback document
        """
        try:
            feedback = await Feedback.find_one(
                Feedback.sid == ObjectId(story_id),
                Feedback.uid == user_id
            )
            if not feedback:
                raise NotFoundError("Feedback not found")
            return feedback
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting feedback: {e}")
            raise Exception(f"Failed to get feedback: {str(e)}")


story_service = StoryService()

