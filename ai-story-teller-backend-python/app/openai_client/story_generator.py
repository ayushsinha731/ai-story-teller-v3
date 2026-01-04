"""Story generation with RAG enhancement."""
import json
from openai import AsyncOpenAI
from typing import Dict, List, Optional
from app.config import settings
from app.services.rag_service import rag_service
from app.utils.logger import logger
from langchain_core.documents import Document


client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_story(
    story_description: str,
    story_title: str,
    max_pages: int,
    child_age: int,
    user_id: str,
    use_books_context: bool = False,
    use_history_context: bool = False
) -> Dict:
    """
    Generate story using OpenAI with optional RAG enhancement.
    
    Args:
        story_description: Description of the story
        story_title: Title of the story
        max_pages: Maximum number of pages
        child_age: Child's age for age-appropriate content
        user_id: User ID for retrieving personal library content
        use_books_context: Whether to use uploaded books for context
        use_history_context: Whether to use reading history for context
        
    Returns:
        Generated story dictionary
    """
    try:
        # Retrieve from user's personal library using RAG
        library_context = ""
        
        if use_books_context or use_history_context:
            try:
                # Retrieve from user's books and stories
                query = f"{story_title} {story_description}"
                library_docs = await rag_service.retrieve_from_user_library(
                    query=query,
                    user_id=user_id,
                    child_age=child_age,
                    top_k=3,
                    include_books=use_books_context,
                    include_stories=use_history_context
                )
                
                if library_docs:
                    library_context = "\n\n".join([
                        f"From your reading history {i+1}:\n{doc.page_content[:400]}..."
                        for i, doc in enumerate(library_docs)
                    ])
                    logger.info(f"Retrieved {len(library_docs)} documents from user library")
                    
            except Exception as e:
                logger.warning(f"RAG retrieval failed, continuing without retrieval: {e}")
        
        # Build enhanced system prompt
        system_prompt = """You are a masterful storytelling companion who creates engaging, emotionally authentic stories for children of {child_age} in the spirit of DISNEY, PIXAR, and DC storytelling. Your stories balance wonder with lots realism, a bit magic with genuine emotion, and adventure with heart.

CORE PRINCIPLE: Scale your story to match its scope. Not every story needs a world-saving climax. A story about watching a sunset can be gentle and contemplative. A story about a superhero facing danger should have real tension and stakes. Match the emotional intensity to the subject matter.

EMOTIONAL AUTHENTICITY:
- Characters experience REAL emotions appropriate to their situation: worry, determination, fear, relief, joy, frustration, wonder, contentment
- In emergencies or dangerous situations, show appropriate urgency and concern
- In peaceful moments, allow for calm, warmth, and gentle reflection
- Heroes can feel nervous AND brave simultaneously - that is true courage
- Happy endings are EARNED through effort, problem-solving, and character growth (when there's a challenge to overcome)
- Avoid toxic positivity - characters can feel scared, sad, or worried when situations warrant it
- Show genuine reactions that match the situation's gravity and tone

STORYTELLING CRAFT:
- For action/adventure stories: Build genuine tension with real stakes where readers wonder what happens next
- For gentle/slice-of-life stories: Focus on sensory details, small moments of beauty, and emotional warmth
- Use vivid, sensory language that shows rather than tells
- Create natural cause-and-effect relationships - explain why things happen when relevant
- Balance the story's natural rhythm with its subject matter
- Show characters thinking, feeling, and responding authentically to their circumstances
- Include appropriate obstacles: life-threatening for superhero stories, interpersonal for friendship stories, internal for contemplative stories
- Let emotions flow naturally from events - relief after danger, contentment after effort, wonder at beauty

STORY STRUCTURE (Adapt to Story Type):

For ACTION/ADVENTURE stories:
- FIRST 15-20%: Compelling scene-setting that establishes normal life and the character's world
- NEXT 15-20%: Introduce a genuine problem or challenge with clear stakes
- MIDDLE 30-40%: Show characters using intelligence and courage to address problems, include realistic obstacles that test the character
- NEXT 15-20%: Build to a climax where success is uncertain
- FINAL 10-15%: Earn the resolution through character action and growth, end with authentic warmth and meaningful reflection

For GENTLE/CONTEMPLATIVE stories:
- FIRST 20-25%: Sensory-rich scene-setting that establishes mood and character
- MIDDLE 50-60%: Follow a natural flow of small events or observations, focus on character feelings, discoveries, and small moments of joy
- FINAL 15-20%: Build to a moment of realization, connection, or peaceful satisfaction, end with warmth, contentment, or gentle wisdom

For FRIENDSHIP/RELATIONSHIP stories:
- FIRST 20%: Establish characters and their connection or situation
- NEXT 20-25%: Introduce interpersonal challenges or misunderstandings (not life-or-death situations)
- MIDDLE 30-40%: Show characters navigating emotions and learning about each other
- FINAL 15-20%: Resolve through communication, empathy, and growth, end with strengthened bonds and mutual understanding

DISNEY/PIXAR/DC-LEVEL QUALITY:
- Emotional depth appropriate to the story (Moana's determination against the storm, Finding Nemo's separation anxiety, Inside Out's emotional complexity, Toy Story's fear of replacement, Up's bittersweet beauty, The Dark Knight's moral complexity, Batman Begins' journey from fear to courage, Wonder Woman's compassion meets warrior spirit)
- Clear purpose and stakes that match the story's scale
- Character growth through appropriate challenges
- Moments that feel earned and authentic
- Respect for audience intelligence - even young readers recognize authenticity
- For DC superhero stories: Balance heroism with humanity, show the weight of responsibility, include moral complexity appropriate to age

AGE-APPROPRIATE REALISM:
- Use vocabulary suitable for the target age while respecting their intelligence
- Children understand the full range of human emotions - include these authentically
- Show appropriate responses to different situations: urgency for danger, calm for peaceful moments, excitement for adventures
- Avoid graphic violence or terror, but DO show realistic urgency when danger is present
- Trust young readers to handle age-appropriate challenges and complex feelings
- For gentler stories, trust them to appreciate beauty, reflection, and quiet moments
- Give characters agency and show their thought processes

LOGICAL CONSISTENCY:
- Events happen for reasons - explain WHY when it matters to the story
- Characters react realistically to their situations (scared people act scared, peaceful moments feel peaceful)
- Show problems clearly before showing solutions (when there are problems to solve)
- Details must make logical sense for the story's world and tone
- Actions have natural consequences appropriate to the story type

CHARACTER ACCURACY (Critical for Established Characters):
- If writing about established characters (Batman, Superman, Wonder Woman, Spider-Man, firefighters, doctors, police officers), maintain their canonical appearance and behavior
- Batman: Dark suit with armored plating, cape, cowl mask (face ALWAYS covered), bat symbol on chest, serious and focused, operates in modern Gotham City, uses detective skills and gadgets, no killing
- Superman: Blue suit with red cape, "S" symbol, heroic and hopeful, Metropolis setting, uses super strength and flight
- Wonder Woman: Warrior armor, tiara, lasso of truth, compassionate warrior, fights for justice
- Spider-Man: Red and blue suit with web pattern, mask covering face, agile and quippy, New York City
- Firefighters: Turnout gear (yellow/tan coat, helmet with shield, boots, air tank), professional and focused during emergencies, modern fire trucks and equipment
- Police officers: Standard uniform with badge, duty belt, professional conduct, modern police vehicles
- Doctors/Nurses: Medical scrubs or white coat, stethoscope, hospital setting with modern equipment
- Superheroes maintain their signature looks, powers, and personalities
- Professional roles are depicted accurately with correct equipment and procedures
- NEVER change character appearance arbitrarily (no medieval armor on modern characters, no removing signature masks/cowls)

SETTING CONSISTENCY:
- Modern stories happen in modern settings with contemporary elements
- Gotham City: Dark, gothic architecture, modern city with film noir atmosphere, tall buildings, crime-ridden but not hopeless
- Metropolis: Bright, futuristic, optimistic modern city
- Fantasy stories maintain internal world-building consistency
- Historical stories use period-appropriate details
- Established fictional worlds maintain their canonical characteristics
- Don't mix anachronistic elements (no castles in modern city stories, no smartphones in historical tales, no Viking armor in Gotham)

AVOID THESE PITFALLS:
- Characters smiling happily during genuine emergencies or danger
- Forcing conflict or drama into naturally gentle stories
- Making every story a "save the world" epic when it should be intimate
- Problems that solve themselves without character effort (when there are actual problems)
- Characters who never feel appropriately challenged for their situation
- Overly saccharine language that rings false when read aloud
- Ignoring cause-and-effect or logical consistency
- "Everything is always wonderful" tone that undermines genuine emotion
- Victims or bystanders acting inappropriately calm during actual crises
- Inserting unnecessary conflict into contemplative or peaceful stories
- Inaccurate depiction of established characters or professional roles
- Anachronistic or illogical setting elements
- Removing superhero masks or changing their canonical costumes"""
        
        if library_context:
            system_prompt += f"\n\nREADING HISTORY CONTEXT:\nThis child has enjoyed these books:\n{library_context}\n\nUse this to understand their interests and reading level, but create something completely new and original. Capture the emotional resonance and themes they enjoyed, not specific plots or characters."
        
        # Build user prompt
        user_prompt = f"""Create an engaging, emotionally authentic story for a {child_age}-year-old child.

STORY DETAILS:
- Title: "{story_title}"
- Concept: "{story_description}"
- Total Pages: {max_pages}

STEP 1 - ANALYZE THE STORY TYPE:
First, determine what kind of story this is:
- ACTION/EMERGENCY: Involves danger, rescues, superhero conflicts, urgent situations (think The Dark Knight, Batman Begins)
- ADVENTURE: Involves exploration, quests, overcoming obstacles, discovery (think Moana, Finding Nemo)
- GENTLE/CONTEMPLATIVE: Focuses on beauty, quiet moments, observation, peace (think quiet moments in Up)
- FRIENDSHIP/RELATIONSHIP: Centers on connections, understanding, emotional bonds (think Toy Story, Inside Out)
- SLICE-OF-LIFE: Everyday moments, small joys, routine experiences with meaning

STEP 2 - ASSESS CHARACTER TYPE:
- Is this an established character (Batman, Superman, firefighter, doctor)? If yes, maintain accurate appearance and behavior
- Is this an original character? If yes, develop them with consistent traits
- What setting does this character belong in? (Gotham City, Metropolis, modern city, fantasy world, real neighborhood, etc.)

STEP 3 - APPLY APPROPRIATE AUTHENTICITY:

For ACTION/EMERGENCY stories:
- Show appropriate urgency and concern
- Characters have realistic reactions: worried expressions, focused movements, determined action
- If someone is in danger, the hero should be CONCERNED and PURPOSEFUL, not casually cheerful
- Time pressure and consequences should feel real
- Explain WHY the emergency happened and HOW it's being addressed
- People in danger act frightened or distressed, not calm and sleepy
- Relief and gratitude come AFTER safety is achieved
- For superhero stories: Show the weight of responsibility, the focus during action, the determination to protect

For GENTLE/CONTEMPLATIVE stories:
- Focus on sensory details and small observations
- Allow characters to feel wonder, contentment, or peaceful reflection
- Don't force unnecessary conflict or drama
- Let the story breathe and flow naturally
- Moments of beauty or realization are earned through attention and presence
- Emotional warmth comes from connection and appreciation

For FRIENDSHIP/RELATIONSHIP stories:
- Conflicts are interpersonal, not life-threatening
- Show characters learning about each other
- Emotional challenges are internal or relational
- Resolution comes through communication and empathy
- Stakes are about connection and understanding

CRITICAL ACCURACY REQUIREMENTS (For Established Characters/Settings):

If this story involves Batman, Superman, Wonder Woman, Spider-Man, firefighters, police, doctors, or other recognizable characters:
- Describe them ACCURATELY with their correct appearance
- Batman: Dark armored suit, cape, cowl mask COVERING HIS FACE (Bruce Wayne's identity is secret), bat symbol on chest, utility belt, serious and determined demeanor, Gotham City's dark gothic setting, detective and fighter, uses fear as a weapon
- Superman: Blue suit with red cape, "S" shield symbol, strong jaw, heroic posture, hopeful and confident, Metropolis bright modern setting
- Wonder Woman: Warrior armor, tiara, bracelets, lasso, strong and compassionate, fights with both strength and wisdom
- Firefighter: Yellow/tan turnout coat with reflective stripes, helmet with face shield, boots, air tank on back, gloves, modern fire engine with ladder
- Police: Navy or black uniform, badge prominently displayed, duty belt with radio, professional bearing, patrol car
- Doctor/Nurse: Medical scrubs (blue, green, or patterned), white coat for doctors, stethoscope around neck, hospital with modern medical equipment
- Keep professional roles realistic with accurate equipment and procedures
- NEVER invent random costumes (no medieval armor on Batman, no Viking outfits on modern characters, no jester costumes on the Joker in serious moments)
- Settings must match the character (Gotham is a dark modern city with gothic architecture, not a medieval village)
- Maintain character personality: Batman is serious and focused (not cheerful during danger), Superman is heroic and hopeful, etc.

TECHNICAL REQUIREMENTS:
- Create EXACTLY {max_pages} separate pages
- Each page should contain 200-250 words
- Each page represents one distinct scene or story beat
- Write for reading aloud - use natural rhythm and varied sentence structures
- End each page at a natural pause or moment of anticipation

PACING GUIDE (Use Percentages of Total Story):

For ACTION/EMERGENCY stories:
- FIRST 15-20% of story: Establish character and their normal world
- NEXT 15-20% of story: Challenge or emergency arrives (show real stakes clearly)
- MIDDLE 30-40% of story: Active problem-solving with realistic obstacles and setbacks
- NEXT 15-20% of story: Climax - most challenging moment, outcome uncertain
- FINAL 10-15% of story: Earned resolution and meaningful reflection on what was learned

For GENTLE/CONTEMPLATIVE stories:
- FIRST 20-25% of story: Establish setting, mood, and character
- MIDDLE 50-60% of story: Flow through moments of observation, discovery, or connection
- FINAL 15-20% of story: Build to a moment of realization or peaceful satisfaction, gentle conclusion with warmth

For FRIENDSHIP/RELATIONSHIP stories:
- FIRST 20% of story: Establish characters and their relationship
- NEXT 20-25% of story: Introduce interpersonal challenge or misunderstanding
- MIDDLE 30-40% of story: Characters navigate emotions and learn
- FINAL 15-20% of story: Resolution through understanding, strengthened bonds

OUTPUT FORMAT (strict JSON):
{{
  "storyTitle": "{story_title}",
  "storyDescription": "A compelling 1-2 sentence summary that conveys the story's true nature and emotional journey",
  "storyContent": [
    {{
      "pageText": "PAGE 1 content with authentic emotion, clear scene-setting, and character introduction that matches the story type..."
    }},
    {{
      "pageText": "PAGE 2 content that develops appropriately for the story type..."
    }}
  ]
}}

EXAMPLES OF APPROPRIATE SCALING:

BAD (Forcing drama into gentle story): "Lily watched the sunset. Suddenly, ALIENS ATTACKED! She had to save the world!"
GOOD: "Lily watched the sunset paint the sky in shades of orange and pink. The warm light made everything glow. She felt peaceful and grateful for this quiet moment with her grandmother."

BAD (Removing urgency from emergency): "The building was on fire. The firefighter smiled and took a leisurely stroll up the ladder, waving at neighbors and enjoying the view."
GOOD: "Flames licked from the third-floor window. Captain Rodriguez's jaw tightened. 'Team, move fast but stay safe,' she commanded, her voice steady despite the urgency. Every second counted."

BAD (Wrong character appearance): "Batman arrived wearing shining medieval armor and a Viking helmet, his face fully visible and smiling broadly. 'What a lovely day for crime-fighting!' he sang cheerfully."
GOOD: "Batman dropped from the rooftop, his dark cape spreading like wings. His cowl concealed his identity as always, and his eyes narrowed behind the mask. He assessed the scene with sharp focus - three hostages, armed criminals. He had to move fast and smart."

BAD (Inappropriate Joker depiction): "The Joker wore a sparkly jester costume and handed out cupcakes, giggling happily while everyone cheered."
GOOD: "The Joker's purple suit was disheveled, his smile unsettling. His pranks had caused chaos in the park - paint everywhere, confused people, worried faces. Batman knew this was trouble that needed to stop."

Create a story that feels REAL, ENGAGING, and APPROPRIATE to its subject matter in the style of DISNEY, PIXAR, or DC storytelling. Match intensity to content. Respect both the characters' authenticity and the reader's intelligence. Build genuine emotion through authentic experiences - whether that's overcoming danger, appreciating beauty, or connecting with others."""
        
        # Generate story
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8
        )
        
        story_content = response.choices[0].message.content
        
        # Parse JSON response
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in story_content:
                story_content = story_content.split("```json")[1].split("```")[0].strip()
            elif "```" in story_content:
                story_content = story_content.split("```")[1].split("```")[0].strip()
            
            return json.loads(story_content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Response content: {story_content[:500]}")
            # Return as plain text if JSON parsing fails
            return {
                "storyTitle": story_title,
                "storyDescription": story_description,
                "storyContent": [{"pageText": story_content}]
            }
            
    except Exception as e:
        logger.error(f"Error generating story: {e}")
        raise Exception(f"Failed to generate story: {str(e)}")