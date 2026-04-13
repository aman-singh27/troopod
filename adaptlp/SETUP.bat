@echo off
REM AdaptLP Setup Script - Complete Build & Configuration

echo.
echo 🚀 AdaptLP - AI Landing Page Personalizer Setup
echo ================================================
echo.

REM Check Python
echo 📋 Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.11+
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python %python_version% found

REM Setup Backend
echo.
echo 🔧 Setting up Backend...
cd backend

if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo   Installing dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo   Creating .env file...
    copy .env.example .env >nul 2>&1 || (
        (
            echo GEMINI_API_KEY=your_key_here
            echo FRONTEND_URL=http://localhost:5173
        ) > .env
    )
    echo   ⚠️  IMPORTANT: Add your GEMINI_API_KEY to backend\.env
    echo      You can get a free key at: https://aistudio.google.com/app/apikey
)

cd ..

REM Setup Frontend
echo.
echo 🎨 Setting up Frontend...
cd frontend

echo   Installing npm dependencies...
call npm install --silent

if not exist ".env" (
    echo   ✓ .env already configured (VITE_API_URL=http://localhost:8000^)
)

cd ..

echo.
echo ✅ Setup Complete!
echo.
echo 📖 Next Steps:
echo.
echo 1. Backend Setup:
echo    cd backend
echo    venv\Scripts\activate
echo    REM Edit .env and add GEMINI_API_KEY
echo    python -m uvicorn app.main:app --reload
echo.
echo 2. Frontend Setup (in new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Test the Application:
echo    Open http://localhost:5173 in your browser
echo    Upload an ad image or provide ad URL
echo    Enter a landing page URL (e.g., https://troopod.io)
echo    Click 'Generate Personalized Page'
echo.
echo 🔗 API Documentation: http://localhost:8000/docs (after backend starts)
echo.
pause
