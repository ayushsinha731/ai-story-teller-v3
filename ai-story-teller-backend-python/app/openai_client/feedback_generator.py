"""Feedback generation for story comprehension answers."""
import json
from openai import AsyncOpenAI
from typing import List, Dict
from app.config import settings
from app.utils.logger import logger

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_feedback(questions: List[Dict], story_content: List[Dict]) -> Dict:
    """
    Generate feedback for user answers.
    
    Args:
        questions: List of questions with user answers
        story_content: List of story page content
        
    Returns:
        Dictionary with feedback results
    """
    try:
        # Combine story content
        whole_story = " ".join([page.get("pageText", "") for page in story_content])
        
        system_prompt = """You are a supportive reading assistant focused on enhancing children's reading comprehension. 
        You will be given the full story, the question, the child's answer, 
        and the correct answer. Use this information to compare the child's response with the correct answer and assess their understanding. 
        Provide constructive and encouraging feedback that highlights key areas for improvement, 
        helping the child connect with important details and themes in the story. Offer a rating to indicate their comprehension level, and keep the feedback positive and motivating to foster a love for reading."""
        
        # Build questions prompt
        questions_prompt = "\n".join([
            f"{i+1}. Question: \"{q.get('question', '')}\"\n   - Correct Answer: \"{q.get('answer', '')}\"\n   - User's Answer: \"{q.get('userAnswer', '')}\""
            for i, q in enumerate(questions)
        ])
        
        user_prompt = f"""Evaluate the user's responses to the following questions based on the provided story.

Full Story:
"{whole_story}"

Questions and Answers:
{questions_prompt}

For each question, provide:
1. A rating out of 5 based on how accurately the user's answer shows understanding of the story.
2. Constructive feedback that helps the child improve their comprehension skills.
3. Positive reinforcement to keep the child motivated.

**Output the results in strict JSON format** as shown below:

{{
  "results": [
    {{
      "question": "Question text here",
      "rating": 4,
      "answer": "Correct answer here",
      "userAnswer": "User's answer here",
      "feedback": "Feedback text here",
      "positiveReinforcement": "Positive reinforcement text here"
    }}
  ]
}}

Generate feedback for all {len(questions)} questions. Remember to keep the feedback child-friendly and focused on helping them build reading comprehension skills."""
        
        response = await client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        data = response.choices[0].message.content
        sanitized_data = data.strip().replace("\r\n", "").replace("\n", "")
        
        # Try to extract JSON from markdown
        if "```json" in sanitized_data:
            sanitized_data = sanitized_data.split("```json")[1].split("```")[0].strip()
        elif "```" in sanitized_data:
            sanitized_data = sanitized_data.split("```")[1].split("```")[0].strip()
        
        try:
            feedback = json.loads(sanitized_data)
            return feedback
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {sanitized_data[:500]}")
            raise Exception(f"Failed to parse feedback: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error generating feedback: {e}")
        raise Exception(f"Failed to generate feedback: {str(e)}")

