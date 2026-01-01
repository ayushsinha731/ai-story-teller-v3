#!/bin/bash

# AI Story Teller - Quick Setup Script

echo "🚀 AI Story Teller - Docker Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Desktop."
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Check if .env file exists
if [ ! -f "ai-story-teller-backend-python/.env" ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env file from .env.example..."
    
    if [ -f "ai-story-teller-backend-python/.env.example" ]; then
        cp ai-story-teller-backend-python/.env.example ai-story-teller-backend-python/.env
        echo "✅ Created .env file"
        echo ""
        echo "⚠️  IMPORTANT: Please edit ai-story-teller-backend-python/.env and add your API keys:"
        echo "   - OPENAI_API_KEY"
        echo "   - ASSEMBLY_AI_API_KEY"
        echo "   - AWS credentials (S3)"
        echo "   - Cloudinary credentials"
        echo "   - JWT_SECRET (use a random string)"
        echo ""
        read -p "Press Enter after you've updated the .env file..."
    else
        echo "❌ .env.example not found. Please create .env file manually."
        exit 1
    fi
else
    echo "✅ .env file exists"
fi

echo ""
echo "🐳 Starting Docker containers..."
echo ""

# Build and start containers
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to be healthy..."
echo ""

# Wait for services to be healthy
sleep 5

# Check service status
docker-compose ps

echo ""
echo "📊 Service Logs:"
echo "================"
docker-compose logs --tail=20

echo ""
echo "✨ Setup Complete!"
echo ""
echo "Access the application at:"
echo "  🌐 Frontend: http://localhost"
echo "  🔌 Backend API: http://localhost:8000"
echo "  📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "  📋 View logs: docker-compose logs -f"
echo "  🔄 Restart: docker-compose restart"
echo "  🛑 Stop: docker-compose down"
echo ""
