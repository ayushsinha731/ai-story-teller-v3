"""Audio service for audio processing and management."""
from typing import Optional
from bson import ObjectId
import assemblyai as aai
from jiwer import wer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from openai import AsyncOpenAI
from app.schemas.audio import Audio
from app.schemas.story import Story
from app.utils.s3_client import s3_client
from app.config import settings
from app.exceptions import NotFoundError
from app.utils.logger import logger
import difflib

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

# Configure AssemblyAI
aai.settings.api_key = settings.assembly_ai_api_key
openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


class AudioService:
    """Service for audio-related operations."""
    
    @staticmethod
    async def upload_audio_to_s3(
        audio_file: bytes,
        file_name: str,
        story_id: str
    ) -> Audio:
        """
        Upload audio file to S3 and create audio record.
        
        Args:
            audio_file: Audio file bytes
            file_name: Original file name
            story_id: Story ID
            
        Returns:
            Audio document
        """
        try:
            # Get story
            story = await Story.get(story_id)
            if not story:
                raise NotFoundError("Story not found")
            
            # Combine story content
            whole_story = " ".join([page.page_text for page in story.story_content])
            
            # Upload to S3
            s3_key, s3_url = await s3_client.upload_audio(
                file_content=audio_file,
                file_name=file_name,
                folder="audio"
            )
            
            # Create audio document
            audio = Audio(
                file_path=s3_url,
                file_name=file_name,
                s3_key=s3_key,
                s3_bucket=settings.s3_bucket_name,
                whole_story=whole_story,
                sid=ObjectId(story_id)
            )
            await audio.insert()
            
            logger.info(f"Audio uploaded: {audio.id}")
            return audio
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error uploading audio: {e}")
            raise Exception(f"Failed to upload audio: {str(e)}")
    
    @staticmethod
    async def transcribe_audio(audio_url: str) -> str:
        """
        Transcribe audio using AssemblyAI.
        
        Args:
            audio_url: URL of audio file (S3 URL)
            
        Returns:
            Transcribed text
        """
        try:
            transcriber = aai.Transcriber()
            config = aai.TranscriptionConfig()
            transcript = transcriber.transcribe(audio_url, config=config)
            return transcript.text
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    @staticmethod
    async def enhance_transcript(transcript: str, story: str) -> str:
        """
        Enhance transcript using OpenAI for context-aware correction.
        
        Args:
            transcript: Raw transcript from AssemblyAI
            story: Original story text for context
            
        Returns:
            Enhanced transcript
        """
        try:
            completion = await openai_client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are the most important part of word error calculator. You will be given two strings 'content' and 'context'. Context is the corrected expected string and content is the sentence or paragraph spoken by the speaker. Your job is to replace the incorrect or out of context words in the content string with the corrected spelling or within context words in the context string. Your job is not to return the final corrected string, just make necessary changes in the content string and output it, not even a word(or character) extra. You don't have to add words or mess with the punctuation, just correct them"
                    },
                    {
                        "role": "user",
                        "content": f"content: {transcript} context: {story}"
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error enhancing transcript: {e}")
            return transcript  # Return original if enhancement fails
    
    @staticmethod
    def analyze_punctuation(transcript: str, story: str) -> list:
        """
        Analyze punctuation differences between transcript and story.
        
        Args:
            transcript: Transcribed text
            story: Original story text
            
        Returns:
            List of differences
        """
        try:
            transcript_sentences = sent_tokenize(transcript)
            story_sentences = sent_tokenize(story)

            # Analyze punctuation in each sentence
            differences = []
            # We iterate up to the length of the shorter list to avoid index errors
            # Ideally sentences should align, but if not, we compare what we can
            min_len = min(len(transcript_sentences), len(story_sentences))
            
            for i in range(min_len):
                transcript_sentence = transcript_sentences[i]
                story_sentence = story_sentences[i]
                
                transcript_words = word_tokenize(transcript_sentence)
                story_words = word_tokenize(story_sentence)

                # Compare punctuation in each sentence
                transcript_punctuation = [w for w in transcript_words if w in string.punctuation]
                story_punctuation = [w for w in story_words if w in string.punctuation]

                if transcript_punctuation != story_punctuation:
                    differences.append({
                        'sentence_index': i,
                        'transcript_punctuation': transcript_punctuation,
                        'story_punctuation': story_punctuation
                    })
            
            return differences
        except Exception as e:
            logger.error(f"Error analyzing punctuation: {e}")
            return []

    @staticmethod
    def highlight_differences(original_text: str, your_reading: str) -> str:
        """
        Highlight differences between original text and reading.
        
        Args:
            original_text: The original story text
            your_reading: The transcribed text
            
        Returns:
            HTML string with highlighted differences
        """
        try:
            # Generate the differences
            diff = difflib.ndiff(original_text.split(), your_reading.split())

            # Highlight the differences
            highlighted_text = []
            for word in diff:
                if word.startswith("- "):  # Word in original but missing in reading
                    highlighted_text.append(f'<span class="bg-red-200 text-red-700 px-1 rounded">{word[2:]}</span>')
                elif word.startswith("+ "):  # Extra word in reading
                    highlighted_text.append(f'<span class="bg-green-200 text-green-700 px-1 rounded">{word[2:]}</span>')
                else:
                    highlighted_text.append(word[2:])  # No difference

            # Join the list into a single string and return
            return ' '.join(highlighted_text)
        except Exception as e:
            logger.error(f"Error highlighting differences: {e}")
            return ""
    
    @staticmethod
    async def process_audio(audio_id: str) -> dict:
        """
        Process audio: transcribe, enhance, and calculate score.
        
        Args:
            audio_id: Audio document ID
            
        Returns:
            Dictionary with transcript, enhanced_transcript, and score
        """
        try:
            audio = await Audio.get(audio_id)
            if not audio:
                raise NotFoundError("Audio not found")
            
            if not audio.whole_story:
                raise Exception("Story content not found for audio")
            
            # Transcribe audio
            transcript = await AudioService.transcribe_audio(audio.file_path)
            
            # Update transcript in database
            audio.transcript = transcript
            await audio.save()
            
            # Enhance transcript
            enhanced_transcript = await AudioService.enhance_transcript(
                transcript,
                audio.whole_story
            )
            
            # Calculate Word Error Rate (WER) using enhanced transcript
            # Enhanced transcript has context-aware corrections applied
            error_rate = wer(audio.whole_story, enhanced_transcript)
            
            # Convert to score (0-100)
            score = max(0, 100 - (100 * error_rate))
            
            # Update audio document
            audio.score = score
            await audio.save()
            
            # Perform punctuation analysis
            punctuation_analysis = AudioService.analyze_punctuation(transcript, audio.whole_story)
            
            # Generate highlighted differences
            highlighted_diff = AudioService.highlight_differences(audio.whole_story, transcript)
            
            logger.info(f"Audio processed: {audio_id}, score: {score:.2f}")
            
            return {
                "transcript": transcript,
                "enhanced_transcript": enhanced_transcript,
                "score": score,
                "punctuation_analysis": punctuation_analysis,
                "highlighted_diff": highlighted_diff
            }
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            raise Exception(f"Failed to process audio: {str(e)}")
    
    @staticmethod
    async def get_audio_feedback(audio_id: str) -> dict:
        """
        Get audio feedback with story data.
        
        Args:
            audio_id: Audio document ID
            
        Returns:
            Dictionary with audio and story data
        """
        try:
            audio = await Audio.get(audio_id)
            if not audio:
                raise NotFoundError("Audio not found")
            
            story = None
            if audio.sid:
                story = await Story.get(audio.sid)
                if not story:
                    raise NotFoundError("Story not found")
            
            return {
                "audio": audio,
                "story": story
            }
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting audio feedback: {e}")
            raise Exception(f"Failed to get audio feedback: {str(e)}")


audio_service = AudioService()

