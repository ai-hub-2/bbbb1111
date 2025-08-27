#!/bin/bash

# Quick Production Deployment - النشر السريع للإنتاج
# One-command deployment - نشر بضغطة واحدة

echo "🚀 Quick Production Deployment - النشر السريع للإنتاج"
echo "=================================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please update .env file with your real API keys before continuing!"
    echo "   Required: GOOGLE_MERCHANT_API_KEY, OPENAI_API_KEY, CLOUDFLARE_API_TOKEN"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p logs data ssl backups grafana/dashboards grafana/datasources

# Generate SSL certificates
echo "🔐 Generating SSL certificates..."
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=SA/ST=Riyadh/L=Riyadh/O=Super Blue Badge App/CN=localhost"
    chmod 600 ssl/key.pem
    chmod 644 ssl/cert.pem
    echo "✅ SSL certificates generated"
else
    echo "✅ SSL certificates already exist"
fi

# Build and start services
echo "🐳 Building and starting services..."
docker-compose build --no-cache
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check services
echo "🔍 Checking service health..."

# Check main app
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Main application is running"
else
    echo "❌ Main application failed to start"
    echo "📋 View logs: docker-compose logs app"
    exit 1
fi

# Check Nginx
if curl -f http://localhost/health >/dev/null 2>&1; then
    echo "✅ Nginx is running"
else
    echo "❌ Nginx failed to start"
    echo "📋 View logs: docker-compose logs nginx"
    exit 1
fi

# Check database
if docker-compose exec -T db pg_isready -U postgres >/dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
    echo "📋 View logs: docker-compose logs db"
    exit 1
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "❌ Redis failed to start"
    echo "📋 View logs: docker-compose logs redis"
    exit 1
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY! 🎉"
echo "=================================================="
echo ""
echo "📊 Your application is now running at:"
echo "  🌐 Main App:     http://localhost:8000"
echo "  🌐 Web Interface: http://localhost"
echo "  📊 Monitoring:   http://localhost:3000 (admin/admin)"
echo "  📈 Metrics:      http://localhost:9090"
echo ""
echo "🔧 Management commands:"
echo "  📋 View logs:    docker-compose logs -f"
echo "  🛑 Stop:         docker-compose down"
echo "  🔄 Restart:      docker-compose restart"
echo "  📦 Update:       git pull && docker-compose up -d --build"
echo ""
echo "🧪 Run production tests:"
echo "  python3 test_production.py"
echo ""
echo "🚀 Your Super Blue Badge App is now LIVE in production! 🔵✨"
echo ""
echo "⚠️  REMEMBER: Update .env file with your real API keys!"
echo "⚠️  REMEMBER: Change default passwords in production!"
echo "⚠️  REMEMBER: Configure SSL certificates for your domain!"