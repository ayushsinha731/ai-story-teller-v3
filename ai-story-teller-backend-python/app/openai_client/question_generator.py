"""Question generation for story comprehension."""
import json
from openai import AsyncOpenAI
from typing import List, Dict
from app.config import settings
from app.utils.logger import logger

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_questions(story_content: List[Dict], story_title: str) -> Dict:
    """
    Generate comprehension questions for a story.
    
    Args:
        story_content: List of page content dictionaries
        story_title: Title of the story
        
    Returns:
        Dictionary with questions list
    """
    try:
        # Combine all story content
        whole_story = " ".join([page.get("pageText", "") for page in story_content])
        
        system_prompt = """You are a helpful and creative assistant designed to generate engaging and age-appropriate questions for children. Your questions should be fun, imaginative, and suitable for the given story, ensuring they are both entertaining and educational."""
        
        user_prompt = f"""Generate questions and answers for the story "{story_title}" with the story content: \n\n{whole_story}.
        The output should be strictly in JSON format with the following structure:
        {{
          "questions": [
            {{
              "question": "The question you want to ask",
              "answer": "The correct answer which you think is right",
              "userAnswer": ""
            }}
          ]
        }}
        Generate exactly 5 questions. Ensure that the JSON is valid, properly formatted, and contains no additional commentary or explanations."""
        
        response = await client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        questions_text = response.choices[0].message.content
        
        # Sanitize and parse
        sanitized_text = questions_text.strip().replace("\r\n", "").replace("\n", "")
        
        # Try to extract JSON from markdown code blocks
        if "```json" in sanitized_text:
            sanitized_text = sanitized_text.split("```json")[1].split("```")[0].strip()
        elif "```" in sanitized_text:
            sanitized_text = sanitized_text.split("```")[1].split("```")[0].strip()
        
        try:
            questions = json.loads(sanitized_text)
            return questions
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {sanitized_text[:500]}")
            raise Exception(f"Failed to parse questions: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        raise Exception(f"Failed to generate questions: {str(e)}")

