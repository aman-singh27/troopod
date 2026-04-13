#!/bin/bash
# AdaptLP Setup Script - Complete Build & Configuration

set -e

echo "🚀 AdaptLP - AI Landing Page Personalizer Setup"
echo "================================================"
echo ""

# Check Python
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python -m venv venv
fi

source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

echo "  Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp .env.example .env
    echo "  ⚠️  IMPORTANT: Add your GEMINI_API_KEY to backend/.env"
    echo "     You can get a free key at: https://aistudio.google.com/app/apikey"
fi

cd ..

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

echo "  Installing npm dependencies..."
npm install --silent

if [ ! -f ".env" ]; then
    echo "  ✓ .env already configured (VITE_API_URL=http://localhost:8000)"
fi

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📖 Next Steps:"
echo ""
echo "1. Backend Setup:"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   cp .env.example .env"
echo "   # Edit .env and add GEMINI_API_KEY"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "2. Frontend Setup (in new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Test the Application:"
echo "   Open http://localhost:5173 in your browser"
echo "   Upload an ad image or provide ad URL"
echo "   Enter a landing page URL (e.g., https://troopod.io)"
echo "   Click 'Generate Personalized Page'"
echo ""
echo "🔗 API Documentation: http://localhost:8000/docs (after backend starts)"
echo ""
