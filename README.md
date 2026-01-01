# AI Story Teller

An AI-powered educational storytelling platform for children featuring personalized story generation, reading practice with audio analysis, book upload with RAG enhancement, and comprehensive feedback systems.

## 🚀 Features

### Story Generation
- **AI-Powered Creation**: OpenAI GPT-based story generation with customizable parameters
- **RAG Enhancement**: ChromaDB vector store for context-aware story generation
- **Book Upload**: Upload PDF, TXT, or EPUB books to personalize story generation
- **Image Generation**: Optional AI-generated images using Cloudinary

### Reading & Assessment
- **Audio Recording**: Record story readings for analysis
- **Transcription \u0026 Scoring**: AssemblyAI transcription with Word Error Rate (WER) analysis
- **Comprehension Questions**: Auto-generated questions with instant feedback
- **Progress Tracking**: Monitor reading improvement over time

### User Experience
- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Secure Authentication**: JWT-based auth with HTTP-only cookies
- **Real-time Updates**: Interactive feedback and progress visualization

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: MongoDB with Beanie ODM
- **Vector Store**: ChromaDB for RAG
- **AI Services**: OpenAI GPT, AssemblyAI, Cloudinary
- **Storage**: AWS S3 for file uploads
- **Authentication**: JWT with python-jose

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS + Radix UI
- **Routing**: React Router v6
- **Icons**: Lucide React
- **State Management**: React Context

## 📋 Prerequisites

- Docker and Docker Compose (recommended)
- **OR** Manual setup:
  - Python 3.11+
  - Node.js 18+
  - MongoDB
- API Keys (required):
  - OpenAI API key
  - AssemblyAI API key
  - AWS S3 credentials
  - Cloudinary account

## 🚀 Quick Start with Docker

### Option 1: Automated Setup (Recommended)

```bash
cd AIStoryTeller
./setup.sh
```

The setup script will:
- ✅ Check Docker installation
- ✅ Create .env from .env.example template
- ✅ Prompt for API key configuration
- ✅ Build and start all containers

### Option 2: Manual Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AIStoryTeller
```

### 2. Set Up Environment Variables

Copy and edit the example file:

```bash
cp ai-story-teller-backend-python/.env.example ai-story-teller-backend-python/.env
# Edit the .env file with your API keys
```

Or create `.env` file in `ai-story-teller-backend-python/` manually:

```env
# MongoDB
MONGODB_URI=mongodb://mongodb:27017
DATABASE_NAME=ai_story_teller

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=15

# OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# AssemblyAI
ASSEMBLY_AI_API_KEY=your-assemblyai-key

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# Application URLs
FRONTEND_URL=http://localhost
BACKEND_URL=http://localhost:8000

# Other Settings
LOG_LEVEL=INFO
CHROMA_DB_PATH=./chroma_db
CORS_ORIGINS=["http://localhost", "http://localhost:80"]
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean start)
docker-compose down -v
```

**Application will be available at:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🔧 Manual Installation

### Backend Setup

```bash
cd ai-story-teller-backend-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see above)
# Make sure MONGODB_URI points to localhost: mongodb://localhost:27017

# Run the application
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd ai-story-teller-frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_BACKEND_URL=http://localhost:8000" > .env

# Run development server
npm run dev

# Build for production
npm run build
```

## 📁 Project Structure

```
AIStoryTeller/
├── ai-story-teller-backend-python/
│   ├── app/
│   │   ├── main.py                    # FastAPI application
│   │   ├── config.py                  # Configuration
│   │   ├── database.py                # MongoDB connection
│   │   ├── models/                    # Pydantic models
│   │   ├── schemas/                   # Beanie schemas
│   │   ├── routers/                   # API endpoints
│   │   │   ├── users.py
│   │   │   ├── stories.py
│   │   │   ├── audio.py
│   │   │   └── books.py               # Book upload endpoints
│   │   ├── services/                  # Business logic
│   │   │   ├── story_service.py
│   │   │   ├── audio_service.py
│   │   │   ├── book_service.py        # Book processing
│   │   │   └── rag_service.py         # RAG/ChromaDB
│   │   ├── openai_client/             # AI integrations
│   │   ├── middleware/                # Auth middleware
│   │   └── utils/                     # Utilities
│   ├── tests/                         # Test suite
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── ai-story-teller-frontend/
│   ├── src/
│   │   ├── components/                # React components
│   │   │   ├── BookCard.jsx           # Book display
│   │   │   ├── BookUploadModal.jsx    # Upload interface
│   │   │   ├── StoryCard.jsx
│   │   │   └── ...
│   │   ├── pages/                     # Page components
│   │   │   ├── DashboardPage.jsx      # Main dashboard
│   │   │   ├── ReadStoryPage.jsx
│   │   │   ├── AssignmentPage.jsx
│   │   │   └── ...
│   │   ├── context/                   # State management
│   │   ├── lib/                       # Utilities
│   │   └── App.jsx
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── .env
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/user/signup` - User registration
- `POST /api/user/login` - User login
- `POST /api/user/logout` - User logout
- `GET /api/user/me` - Get current user

### Stories
- `POST /api/story/create` - Create AI-generated story
- `GET /api/story/getStory/{sid}` - Get story by ID
- `GET /api/story/stories/{uid}` - Get all user stories
- `GET /api/story/getQuestions/{sid}` - Get assignment questions
- `POST /api/story/feedback/{sid}` - Submit answers
- `GET /api/story/getFeedback/{sid}` - Get feedback

### Books (NEW)
- `POST /api/books/upload` - Upload book file
- `GET /api/books` - Get user's books
- `DELETE /api/books/{book_id}` - Delete book

### Audio
- `POST /upload/{sid}` - Upload audio recording
- `POST /process-audio/{aid}` - Process \u0026 analyze audio
- `GET /audio/finalFeedback/{aid}` - Get audio feedback

## ✨ New Features: Book Upload \u0026 RAG

Parents can now upload their children's books (PDF, TXT, EPUB) which are:
1. Stored in AWS S3
2. Text extracted and indexed in ChromaDB
3. Used to personalize story generation

When creating stories, toggle "Use My Reading History" to generate stories inspired by uploaded books.

## 🧪 Testing

### Backend Tests
```bash
cd ai-story-teller-backend-python
pytest
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd ai-story-teller-frontend
npm run test
```

## 🐛 Troubleshooting

### Docker Issues
```bash
# View container logs
docker-compose logs backend
docker-compose logs frontend

# Restart specific service
docker-compose restart backend

# Rebuild containers
docker-compose up -d --build
```

### MongoDB Connection
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# Connect to MongoDB shell
docker exec -it aistoryteller-mongodb mongosh
```

### ChromaDB Issues
```bash
# Clear ChromaDB (will lose indexed data)
rm -rf ai-story-teller-backend-python/chroma_db/*
```

## 📊 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URI` | MongoDB connection string | Yes |
| `JWT_SECRET` | Secret key for JWT signing | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `ASSEMBLY_AI_API_KEY` | AssemblyAI API key | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes |
| `S3_BUCKET_NAME` | S3 bucket name | Yes |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes |

## 🚀 Deployment

### Using Docker Compose (Recommended)
1. Set up environment variables in production
2. Update `FRONTEND_URL` and `BACKEND_URL` in `.env`
3. Run `docker-compose -f docker-compose.yml up -d`

### Individual Deployments
- **Backend**: Deploy to services like Railway, Render, or AWS ECS
- **Frontend**: Deploy to Vercel, Netlify, or serve from Nginx

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For questions or issues, please open an issue on GitHub.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) for the frontend
- [OpenAI](https://openai.com/) for AI capabilities
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [ChromaDB](https://www.trychroma.com/) for vector storage
