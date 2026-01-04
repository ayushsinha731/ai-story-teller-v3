from typing import TypedDict, Dict, Any, Annotated, Optional
import json
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.rag_service import rag_service
from app.config import settings
from app.utils.logger import logger

# Initialize LLM
llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model="gpt-5-mini",
    temperature=0.7
)

def merge_usage(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
    """Merge two token usage dictionaries."""
    if not a: return b
    if not b: return a
    return {
        "prompt_tokens": a.get("prompt_tokens", 0) + b.get("prompt_tokens", 0),
        "completion_tokens": a.get("completion_tokens", 0) + b.get("completion_tokens", 0),
        "total_tokens": a.get("total_tokens", 0) + b.get("total_tokens", 0)
    }

class StoryState(TypedDict):
    # Input keys
    story_title: str
    story_description: str
    child_age: int
    max_pages: int
    user_id: str
    use_books_context: bool
    use_history_context: bool
    
    # Internal/Output keys
    library_context: Optional[str]
    story_content: Optional[Dict]
    token_usage: Annotated[Dict[str, int], merge_usage]

async def retrieve_context(state: StoryState) -> Dict:
    """Node: Retrieve context from RAG service."""
    try:
        if not (state.get("use_books_context") or state.get("use_history_context")):
            return {"library_context": ""}
            
        query = f"{state['story_title']} {state['story_description']}"
        library_docs = await rag_service.retrieve_from_user_library(
            query=query,
            user_id=state["user_id"],
            child_age=state["child_age"],
            top_k=3,
            include_books=state["use_books_context"],
            include_stories=state["use_history_context"]
        )
        
        context_str = ""
        if library_docs:
            context_str = "\n\n".join([
                f"From your reading history {i+1}:\n{doc.page_content[:400]}..."
                for i, doc in enumerate(library_docs)
            ])
            logger.info(f"Retrieved {len(library_docs)} documents")
            
        return {"library_context": context_str}
        
    except Exception as e:
        logger.error(f"Error in retrieve_context: {e}")
        return {"library_context": ""}

async def generate_story_content(state: StoryState) -> Dict:
    """Node: Generate the story JSON."""
    try:
        # Construct parameters
        child_age = state["child_age"]
        max_pages = state["max_pages"]
        title = state["story_title"]
        desc = state["story_description"]
        library_context = state.get("library_context", "")

        # System Prompt
        system_prompt = """You are a helpful and creative assistant designed to generate engaging and age-appropriate stories for children. Your stories should be fun, imaginative, and suitable for the given age group."""
        
        if library_context:
            system_prompt += f"\n\nThe child has read the following books. You may draw inspiration from themes, styles, or concepts they enjoyed, but create something completely original and unique:\n\n{library_context}"

        # User Prompt
        user_prompt = f"""Generate a story for a child of age {child_age} with the following details:
        - Story Title: "{title}"
        - Story Description: "{desc}"
        - The story should contain a maximum of {max_pages} pages.
        - Each page should have a "pageText" field containing a portion of the story.
        - Each page should have a minimum of 250 words.
        - The response should follow this format:
        
        {{
          "storyTitle": "{title}",
          "storyDescription": "{desc}",
          "storyContent": [
            {{
              "pageText": "Text for page 1"
            }},
            {{
              "pageText": "Text for page 2"
            }}
          ]
        }}
        
        Ensure that the story is age-appropriate for a child of age {child_age}.
        Create an original and unique story.
        Return ONLY valid JSON."""

        # Call LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = await llm.ainvoke(messages)
        
        # Track usage
        usage = response.response_metadata.get("token_usage", {})
        logger.info(f"Token usage for story generation: {usage}")

        content_str = response.content
        
        # Parse JSON
        try:
            # Clean markdown code blocks
            original_content = content_str
            if "```json" in content_str:
                content_str = content_str.split("```json")[1].split("```")[0].strip()
            elif "```" in content_str:
                content_str = content_str.split("```")[1].split("```")[0].strip()
            
            logger.info(f"Parsing story JSON (length: {len(content_str)} chars)")
            story_json = json.loads(content_str)
            
            # Validate structure
            if "storyContent" not in story_json or not isinstance(story_json.get("storyContent"), list):
                raise ValueError("Invalid story structure: missing or invalid storyContent")
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Content preview: {content_str[:500]}...")
            # Better fallback - return error instead of malformed data
            raise Exception(f"Failed to parse story JSON from GPT: {str(e)}")

        return {
            "story_content": story_json,
            "token_usage": usage
        }

    except Exception as e:
        logger.error(f"Error in generate_story_content: {e}")
        raise

# Build Graph
workflow = StateGraph(StoryState)

workflow.add_node("retrieve_context", retrieve_context)
workflow.add_node("generate_story_content", generate_story_content)

workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "generate_story_content")
workflow.add_edge("generate_story_content", END)

story_graph = workflow.compile()

async def run_story_generation(
    story_title: str,
    story_description: str,
    child_age: int,
    max_pages: int,
    user_id: str,
    use_books_context: bool = False,
    use_history_context: bool = False
) -> Dict:
    """Wrapper to run the graph."""
    
    initial_state = {
        "story_title": story_title,
        "story_description": story_description,
        "child_age": child_age,
        "max_pages": max_pages,
        "user_id": user_id,
        "use_books_context": use_books_context,
        "use_history_context": use_history_context,
        "token_usage": {}
    }
    
    result = await story_graph.ainvoke(initial_state)
    
    # Log final usage
    total_usage = result.get("token_usage", {})
    logger.info(f"Total story generation usage: {total_usage}")
    
    return result["story_content"]
