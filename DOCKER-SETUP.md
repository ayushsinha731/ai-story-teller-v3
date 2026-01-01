# AI Story Teller - Docker Setup Guide

## Quick Start

### 1. Prerequisites
- Docker Desktop installed and running
- API keys ready (OpenAI, AssemblyAI, AWS S3, Cloudinary)

### 2. Set Up Environment Variables

Create `.env` file in `ai-story-teller-backend-python/` directory with your API keys:

```env
# MongoDB
MONGODB_URI=mongodb://mongodb:27017
DATABASE_NAME=ai_story_teller

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-to-something-random
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=15

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# AssemblyAI
ASSEMBLY_AI_API_KEY=your-assemblyai-api-key

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-s3-bucket-name

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
# From the AIStoryTeller directory
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4. Access the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Stop the Application

```bash
# Stop all services
docker-compose down

# Stop and remove all data (fresh start)
docker-compose down -v
```

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Rebuild After Changes
```bash
# Rebuild all images
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

### Access Container Shell
```bash
# Backend
docker exec -it aistoryteller-backend /bin/bash

# MongoDB
docker exec -it aistoryteller-mongodb mongosh
```

### Check MongoDB Data
```bash
docker exec -it aistoryteller-mongodb mongosh

# Inside mongosh:
use ai_story_teller
db.users.find()
db.stories.find()
db.books.find()
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 80, 8000, or 27017
lsof -i :80
lsof -i :8000
lsof -i :27017

# Stop the service using that port, then restart docker-compose
```

### Backend Can't Connect to MongoDB
```bash
# Check if MongoDB is healthy
docker-compose ps

# Restart MongoDB
docker-compose restart mongodb

# Check MongoDB logs
docker-compose logs mongodb
```

### Frontend Shows 404 or Blank Page
```bash
# Check if frontend built successfully
docker-compose logs frontend

# Rebuild frontend
docker-compose up -d --build frontend
```

### Clear All Data and Start Fresh
```bash
docker-compose down -v
rm -rf ai-story-teller-backend-python/chroma_db/*
docker-compose up -d --build
```

## Development Workflow

### Making Backend Changes
```bash
# 1. Make your code changes
# 2. Rebuild backend
docker-compose up -d --build backend

# 3. Check logs
docker-compose logs -f backend
```

### Making Frontend Changes
```bash
# 1. Make your code changes
# 2. Rebuild frontend
docker-compose up -d --build frontend

# 3. Clear browser cache and refresh
```

### Adding Python Dependencies
```bash
# 1. Add to requirements.txt
# 2. Rebuild backend
docker-compose up -d --build backend
```

### Adding Node Dependencies
```bash
# 1. Add to package.json
# 2. Rebuild frontend
docker-compose up -d --build frontend
```

## Production Deployment

### Environment Variables
Make sure to update these for production:
- `JWT_SECRET`: Use a strong, random value
- `FRONTEND_URL`: Your production frontend URL
- `BACKEND_URL`: Your production backend URL
- `CORS_ORIGINS`: Update to include your production domain

### Security Checklist
- [ ] Change JWT_SECRET to a strong random value
- [ ] Enable HTTPS (use reverse proxy like Nginx or Traefik)
- [ ] Restrict MongoDB access (use authentication)
- [ ] Set up firewall rules
- [ ] Use environment-specific .env files
- [ ] Enable logging and monitoring
- [ ] Set up automated backups for MongoDB

### Recommended Stack
- **Hosting**: AWS ECS, Google Cloud Run, or DigitalOcean App Platform
- **Database**: MongoDB Atlas (managed service)
- **Reverse Proxy**: Nginx or Traefik with Let's Encrypt
- **Monitoring**: Prometheus + Grafana or Datadog
