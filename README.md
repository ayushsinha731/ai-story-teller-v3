# AiStoryTeller

AiStoryTeller is an AI-powered educational storytelling platform designed to make reading fun, interactive, and personalized for children. We combine advanced AI technology with educational best practices to create engaging stories, assess reading comprehension, and provide detailed feedback.

![AiStoryTeller Banner](./screenshots/banner.png)
> *Screenshot placeholder: Main landing page with app logo and tagline*

## Features

### 1. AI-Powered Story Generation

We generate personalized, age-appropriate stories tailored to your child's interests and reading level.

![Story Generation Interface](./screenshots/story-generation.png)
> *Screenshot placeholder: Story creation modal with title, description, and customization options*

**Key Capabilities:**
- **Customizable Parameters**: You can set the story title, description, page count (1-20 pages), and the child's age.
- **AI-Generated Images**: Option to include DALL-E 3 powered illustrations for each story (every 3rd page).
- **Age-Appropriate Content**: Stories are automatically tailored to the child's age (5-15 years).
- **Rich Text Content**: We ensure a minimum of 250 words per page for substantial reading practice.
- **Cloud Storage**: Images are stored in AWS S3 for reliable, scalable access.

**Technical Details:**
- Powered by OpenAI GPT-5-Mini for natural, engaging narratives.
- LangGraph-based story generation workflow for structured output.
- Intelligent image prompt generation for contextually relevant illustrations.

### 2. RAG-Enhanced Personalization

Make stories truly personal by leveraging your child's reading history and uploaded books.

![Book Library](./screenshots/book-library.png)
> *Screenshot placeholder: Grid view of uploaded books with cover previews*

**Features:**
- **Book Upload**: Support for PDF, TXT, and EPUB formats.
- **Smart Text Extraction**: Automatic text extraction from uploaded books.
- **Vector Indexing**: ChromaDB-powered semantic search for context retrieval.
- **Context Selection**: Choose to use uploaded books, past stories, or both for story inspiration.
- **Personalized Stories**: The AI draws themes and styles from your child's favorite books.

**How It Works:**
1. Upload your child's favorite books (stored in AWS S3).
2. Text is extracted and indexed in our ChromaDB vector database.
3. When generating a story, you can toggle "Refer Uploaded Books" or "Refer Past Stories".
4. The AI retrieves relevant context and creates stories inspired by their reading history.

### 3. Story Generation

Generate age-appropriate stories with DALL-E 3 powered images.

![Story](./screenshots/generated-story.png)
> *Screenshot placeholder: Generated story with title and image*

### 4. Audio Reading Assessment

Record story readings and get instant feedback on pronunciation, fluency, and accuracy.

![Audio Recording Interface](./screenshots/audio-recording.png)
> *Screenshot placeholder: Audio recorder with waveform visualization and record/stop buttons*

![Reading Results 1](./screenshots/reading-results-1.png)
> *Screenshot placeholder: Reading Results part 1*

![Reading Results 2](./screenshots/reading-results-2.png)
> *Screenshot placeholder: Reading Results part 2*

**Capabilities:**
- **Audio Upload**: Record directly in the browser or upload WAV/MP3 audio files.
- **AI Transcription**: High-accuracy speech-to-text conversion.
- **Accuracy Scoring**: Word Error Rate (WER) analysis with context-aware enhancement.
- **Pronunciation Feedback**: Detailed word-level accuracy assessment.

**Scoring Algorithm:**
- Raw transcription is processed for accuracy.
- Context-aware correction using GPT models.
- A scientific WER calculation ensures fair and accurate scoring.

### 5. Comprehension Questions & Feedback

Automated question generation and an intelligent text-based feedback system to reinforce learning.

![Assignment Questions](./screenshots/assignment-question.png)
> *Screenshot placeholder: One of 5 comprehension questions with text input fields*

**Question Generation:**
- **Auto-Generated**: 5 comprehension questions per story.
- **Story-Specific**: Questions tailored to the specific narrative.
- **Multiple Attempts**: Take assessments as many times as needed.

![Feedback Results](./screenshots/feedback-results.png)
> *Screenshot placeholder: Detailed feedback showing end result for each question*

**Intelligent Feedback:**
- **Rating System**: 1-5 star rating per answer (using emojis).
- **Constructive Feedback**: Specific guidance on how to improve understanding.
- **Positive Reinforcement**: Encouraging messages to maintain motivation.
- **Detailed Analysis**: Comparison of the child's answer vs. the correct answer.

![Feedback Results List](./screenshots/feedback-results-list.png)
> *Screenshot placeholder: Zoomed out screenshot of feedback results list*

### 6. Multi-User Management

Secure authentication system with personalized dashboards for each family.

**User Features:**
- **Secure Registration**: Parent email, child name, age, and grade level.
- **JWT Authentication**: HTTP-only cookies for secure session management.
- **Personalized Content**: Each user sees only their own stories, books, and progress.
- **Progress Tracking**: View all past stories and assessment results.

### 7. Beautiful, Responsive UI

A modern, intuitive interface designed for both parents and children.

**Design Features:**
- **Modern Aesthetics**: Clean, colorful design appealing to children.
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile.
- **Intuitive Navigation**: Easy-to-use interface for all age groups.
- **Interactive Elements**: Smooth animations and hover effects.
- **Accessibility**: High contrast, readable fonts, and clear visual hierarchy.

## Architecture

### Tech Stack

#### Backend (FastAPI)
- **Framework**: FastAPI (Python 3.11+)
- **Database**: MongoDB Atlas (external cluster)
- **Vector Store**: ChromaDB for RAG functionality
- **AI Services**:
  - OpenAI GPT-4o-Mini (story generation, text processing) as OpenAI GPT-5-Mini was unstable.
  - OpenAI DALL-E 3 (image generation)
  - AssemblyAI (audio transcription)
- **Cloud Storage**: AWS S3 (images and book files)
- **Authentication**: JWT with HTTP-only cookies
- **ODM**: Beanie for MongoDB
- **Orchestration**: LangChain (RAG & Story Graph)

#### Frontend (React + Vite)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Routing**: React Router v6
- **Icons**: Lucide React
- **State Management**: React Context API
- **HTTP Client**: Native Fetch API

#### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (frontend)
- **API Server**: Uvicorn (ASGI)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- External MongoDB Atlas cluster
- AWS S3 bucket with public read access
- API Keys:
  - OpenAI API key
  - AssemblyAI API key
  - AWS credentials

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd AIStoryTeller
```

2. **Configure environment variables**

Create `.env` file in `ai-story-teller-backend-python/`:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=ai_story_teller

# JWT
JWT_SECRET=your-super-secret-jwt-key-min-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=15

# OpenAI
OPENAI_API_KEY=sk-proj-...

# AssemblyAI
ASSEMBLY_AI_API_KEY=...

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# Application URLs
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000

# Other Settings
LOG_LEVEL=INFO
CHROMA_DB_PATH=./chroma_db
CORS_ORIGINS=["http://localhost:5173", "http://localhost", "http://localhost:80"]
```

3. **Start the application**

```bash
# Build and start all containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

4. **Access the application**
- Frontend: http://localhost (port 80)
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Security Features

- **JWT Authentication**: Secure token-based auth with HTTP-only cookies.
- **CORS Protection**: Configured allowed origins.
- **Password Hashing**: Bcrypt for secure password storage.
- **Input Validation**: Pydantic models for request validation.
- **SQL Injection Protection**: MongoDB parameterized queries via Beanie.
- **XSS Protection**: React's built-in escaping.

## Future Improvements

### Custom Speech-to-Text Model
We are planning to replace AssemblyAI with a custom speech-to-text model. This will provide greater control over the transcription process, reduce dependencies on external APIs, and allow us to fine-tune the model specifically for children's speech patterns.

### Enhanced Audio Scoring Algorithm
Implement Character Error Rate (CER) + Word Error Rate (WER) Hybrid scoring for more nuanced reading assessment:

```python
from jiwer import wer, cer

# Calculate both metrics
word_error_rate = wer(whole_story, enhanced_transcript)
char_error_rate = cer(whole_story, enhanced_transcript)

# Weighted combination (70% WER, 30% CER)
combined_error = (0.7 * word_error_rate) + (0.3 * char_error_rate)
score = max(0, 100 - (100 * combined_error))
```

**Benefits**:
- More sensitive to spelling and pronunciation errors.
- Better for young readers with partial correctness.
- Reduces penalty for minor mistakes while maintaining accuracy standards.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) - GPT-5-Mini and DALL-E 3
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) - Frontend framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [AssemblyAI](https://www.assemblyai.com/) - Speech recognition
- [MongoDB Atlas](https://www.mongodb.com/atlas) - Cloud database
- [AWS S3](https://aws.amazon.com/s3/) - Object storage
