"""Image generation using OpenAI DALL-E."""
from openai import AsyncOpenAI
from app.config import settings
from app.utils.logger import logger

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_image(page_text: str, child_age: int = 5, story_title: str = "") -> str | None:
    """
    Generate image for story page using OpenAI DALL-E.
    
    Args:
        page_text: Text content of the page
        child_age: Age of the target child reader
        story_title: Title of the story for character consistency
        
    Returns:
        Image URL or None if generation fails
    """
    try:
        # Create system prompt for image prompt generation
        system_prompt = """You are an expert at creating detailed, accurate image prompts for children's book illustrations in the style of DISNEY, PIXAR, and DC Comics. You MUST maintain absolute character accuracy for established characters.

ABSOLUTE CHARACTER ACCURACY - NON-NEGOTIABLE:

BATMAN (DC Comics):
- ALL BLACK suit with subtle dark gray/charcoal accents - NO OTHER COLORS on the suit
- Black cape that is dark and imposing
- Black cowl/mask that covers entire head and face except jaw and mouth - pointed bat ears on top
- YELLOW oval belt with pouches (or black utility belt in some versions)
- Large BLACK BAT SYMBOL on chest (may have yellow oval background in some versions, but bat itself is BLACK)
- NO blue capes, NO golden emblems, NO bird symbols, NO armor plating with gold trim
- NO fantasy warrior aesthetic - Batman is a modern crime fighter in tactical suit
- Strong, athletic build but human proportions
- Serious, determined expression (when jaw is visible)
- Gotham City: Dark, gothic modern city with Art Deco buildings, NOT fantasy or medieval

SUPERMAN (DC Comics):
- BLUE suit with RED cape
- RED and YELLOW "S" symbol on chest
- RED boots
- Strong heroic build
- Hopeful, confident expression
- Metropolis: Bright, modern, futuristic city

WONDER WOMAN (DC Comics):
- RED and GOLD armor with BLUE skirt/shorts
- Golden tiara with red star
- Silver bracelets
- Golden lasso
- Strong warrior but compassionate expression
- Greek-inspired armor details

SPIDER-MAN (Marvel):
- RED and BLUE suit with black web pattern
- Large white eye pieces on mask
- Spider symbol on chest
- Agile, dynamic poses
- New York City setting with skyscrapers

FIREFIGHTER (Real profession):
- TAN or YELLOW turnout coat with REFLECTIVE YELLOW/SILVER STRIPES
- Helmet: typically yellow, red, or white with front shield showing number/department
- Heavy black boots with steel toes
- Black or yellow pants with reflective stripes
- SCBA (air tank) on back with straps
- Gloves (usually black or tan)
- Modern fire engine: RED with chrome details, ladder, hoses
- Focused, professional demeanor during emergencies

POLICE OFFICER (Real profession):
- NAVY BLUE or BLACK uniform
- Silver or gold badge prominently displayed on chest
- Duty belt with radio, handcuffs, flashlight
- Police cap or no hat
- Black polished shoes
- Modern police car: typically black and white, or dark blue
- Professional, alert bearing

DOCTOR/NURSE (Real profession):
- Medical scrubs: solid colors (blue, green, burgundy) or patterns
- White coat for doctors (optional)
- Stethoscope around neck
- ID badge clipped to scrubs
- Comfortable medical shoes
- Hospital setting with medical equipment, clean modern environment

VISUAL STYLE REQUIREMENTS:
- Modern digital illustration matching DISNEY/PIXAR/DC storybook quality
- Rich, vibrant colors appropriate to the character
- Proper lighting that enhances mood and character recognition
- Professional children's book illustration quality
- Clear composition with strong focal point
- Detailed but not cluttered environments

SCENE ACCURACY:
- Show the EXACT ACTION described in the text
- Character body language must match the emotional state
- Include only props and details mentioned or implied in the text
- Proper perspective and depth
- Visual mood MUST match narrative mood

SETTING CONSISTENCY:
- Modern superhero stories: Contemporary city with modern architecture
- Professional stories: Accurate modern equipment and settings
- Fantasy stories: Consistent internal world-building
- NO mixing of anachronistic elements

STRICT PROHIBITIONS - NEVER DO THESE:
- Changing Batman's black suit to blue, gold, purple, or any other color
- Adding golden bird emblems or fantasy elements to Batman
- Removing superhero masks or cowls
- Putting modern characters in medieval armor or settings
- Making Batman look like a fantasy warrior or knight
- Adding random decorative elements that don't match the character
- Changing professional uniforms to incorrect colors or styles
- Having characters smile inappropriately during tense scenes
- Mixing modern and historical elements incorrectly

QUALITY STANDARDS:
- Illustration should look like it came from an official DISNEY/PIXAR/DC storybook
- Character should be instantly recognizable
- Setting should support the story without overwhelming it
- Colors should be rich but appropriate to the character's palette
- Composition should guide the eye to the main action"""
        
        # Create user prompt to extract visual elements
        user_prompt = f"""Create a DALL-E prompt for a children's book illustration based on this story page.

STORY TITLE: {story_title}
TARGET AGE: {child_age} years old

STORY TEXT:
{page_text}

CRITICAL ANALYSIS REQUIRED:

Step 1 - CHARACTER IDENTIFICATION:
- Does this story feature Batman, Superman, Wonder Woman, Spider-Man, or other established characters?
- Does this feature real professionals (firefighters, police, doctors)?
- If YES to either: You MUST use their EXACT canonical appearance

Step 2 - SETTING IDENTIFICATION:
- Where does this scene take place?
- What time period? (Modern, historical, fantasy)
- What's the environmental context?

Step 3 - ACTION IDENTIFICATION:
- What SPECIFIC action is happening RIGHT NOW in this moment?
- What is the character doing physically?
- What is their emotional state?

Step 4 - MOOD ASSESSMENT:
- Is this tense, peaceful, exciting, contemplative?
- Should the lighting be dramatic, soft, bright?
- What colors support this mood?

CREATE YOUR DALL-E PROMPT (250-350 words):

MANDATORY STRUCTURE:
"Professional children's book illustration in DISNEY/PIXAR/DC storybook style: 

[CHARACTER DESCRIPTION - Be SPECIFIC and ACCURATE]:
- If Batman: "Batman in his iconic ALL BLACK suit with black cape and black cowl mask covering his face (pointed bat ears visible), large black bat symbol on chest, yellow utility belt"
- If firefighter: "Firefighter in tan/yellow turnout coat with reflective stripes, helmet, black boots, SCBA air tank on back"
- If original character: Detailed description with consistent traits
- Current expression and body language matching the emotion

[ACTION - What's happening NOW]:
- Specific physical action being performed
- How the character is positioned
- What they're interacting with

[SETTING - Accurate and detailed]:
- If Gotham: "Dark gothic modern city with Art Deco buildings, nighttime with city lights"
- If hospital: "Modern hospital with medical equipment, clean bright environment"
- Specific environmental details that support the story

[PROPS AND DETAILS]:
- Only items that make sense for this character and scene
- Accurate equipment for professionals
- Story-relevant objects

[LIGHTING AND ATMOSPHERE]:
- Time of day lighting that matches the scene
- Mood-appropriate lighting (dramatic for action, soft for gentle moments)
- Color temperature that enhances the story

[COMPOSITION]:
- Camera angle that best shows the action
- Focal point on the main character/action
- Depth with foreground, midground, background

[COLOR PALETTE]:
- Colors that match the character's canonical appearance
- Supporting environmental colors
- Overall mood through color choices

High quality children's book illustration, rich colors, detailed but clear, emotionally expressive, accurate character design."

VERIFICATION BEFORE FINALIZING:
✓ If Batman: Is he in ALL BLACK? (Not blue, not gold?)
✓ If Batman: Does he have the BLACK bat symbol? (Not a golden bird?)
✓ If firefighter: Tan/yellow gear with reflective stripes? (Not medieval costume?)
✓ Does the setting match the story period and world?
✓ Do props make logical sense for this character?
✓ Does the mood match the text (tense scenes look tense)?
✓ Would a child recognize this character instantly?

CRITICAL REMINDERS:
- Batman's suit is BLACK, not blue or gold or purple
- Batman's symbol is a BLACK BAT, not a golden bird
- Batman wears a COWL that covers his face, showing only jaw
- Gotham is a MODERN CITY with gothic architecture, not a medieval fantasy setting
- Professional uniforms must be accurate to real-world standards
- NO random costume changes or fantasy elements on modern characters

Create your detailed prompt now, ensuring absolute accuracy for any established characters."""
        
        # Get image prompt from GPT with stricter settings
        chat_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        final_prompt = chat_response.choices[0].message.content.strip()
        
        # Add strong enforcement suffix for DALL-E 3
        enhanced_prompt = f"{final_prompt} CRITICAL: Maintain exact character accuracy - Batman in ALL BLACK suit with BLACK bat symbol, firefighters in proper turnout gear, all established characters in their canonical appearance. High quality DISNEY/PIXAR/DC children's book illustration, professional digital art, detailed and expressive, accurate character design, appropriate setting."
        
        logger.info(f"Generated image prompt: {enhanced_prompt[:400]}...")
        
        # Generate image with landscape orientation for better composition
        image_response = await client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            n=1,
            size="1792x1024",
            quality="standard",
            style="vivid"
        )
        
        if image_response.data and len(image_response.data) > 0:
            image_url = image_response.data[0].url
            logger.info("Image generated successfully")
            return image_url
        else:
            logger.error("No image URL returned in response")
            return None
            
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None