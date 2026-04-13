# Quick Start Guide - AdaptLP

## 5-Minute Setup

### Prerequisites
- Python 3.11+ (download from python.org)
- Node.js 18+ (download from nodejs.org)
- A free Gemini API key (get at https://aistudio.google.com/app/apikey)

### Step 1: Get Your Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy the API key

### Step 2: Run Setup Script

**On Windows:**
```bash
SETUP.bat
```

**On macOS/Linux:**
```bash
chmod +x SETUP.sh
./SETUP.sh
```

The script will:
- Check Python installation ✓
- Create Python virtual environment ✓
- Install backend dependencies ✓
- Install frontend dependencies ✓
- Create configuration files ✓

### Step 3: Configure Backend

Edit `backend/.env`:
```
GEMINI_API_KEY=paste_your_api_key_here
FRONTEND_URL=http://localhost:5173
```

### Step 4: Start Services

**Terminal 1 - Backend (port 8000):**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend (port 5173):**
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.0  ready in 234 ms

➜  Local:   http://localhost:5173/
```

### Step 5: Test the Application

1. Open http://localhost:5173 in your browser
2. Scroll to the input form:
   - Upload an ad image OR paste an ad URL
   - Paste a landing page URL
3. Click "Generate Personalized Page"
4. Wait 8-10 seconds while the 4-agent pipeline processes
5. View the personalized landing page with modifications

### Available Endpoints

Once backend is running:

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Personalize API:**
```bash
curl -X POST http://localhost:8000/api/personalize \
  -F "ad_image=@ad.png" \
  -F "landing_page_url=https://example.com"
```

**API Documentation:**
```
http://localhost:8000/docs  (SwaggerUI)
http://localhost:8000/redoc (ReDoc)
```

## Troubleshooting

### Port Already in Use

**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (5173):**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5173 | xargs kill -9
```

### "GEMINI_API_KEY not set"

Edit `backend/.env` and add your API key:
```
GEMINI_API_KEY=sk-...your...key...here
```

### Virtual Environment Issues

Reset and recreate:
```bash
cd backend
rm -rf venv  # or rmdir venv /s /q on Windows
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

### npm Install Failures

Clear cache and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Architecture Overview

```
Frontend (React + Vite)     Backend (FastAPI)           AI Services
─────────────────────       ────────────────            ────────────
  [Home Page]               [FastAPI App]               [Gemini Vision]
      ↓                             ↓                         ↑
  [Ad Input]  ─────────────→  [Agent 1: Analyzer] ──────────↓
  [LP Input]                  [Agent 2: Fetcher]
      ↓                         (Parallel)
  [Processing Timeline]           ↓
      ↓                       [Agent 3: Strategist]
  [Result Page]               [Agent 4: Patcher]
      ←─────────────────────────────→
```

## API Response Structure

```json
{
  "status": "success",
  "ad_analysis": {
    "primary_color": "#FF6B6B",
    "color_palette": ["#FF6B6B", "#FFE66D", "#4ECDC4"],
    "typography": "Sans-serif, Modern"
  },
  "lp_original": {
    "h1": "Original headline",
    "meta_description": "Meta description"
  },
  "modifications": [
    {
      "element_type": "h1",
      "original_text": "Old headline",
      "new_text": "New headline",
      "cro_reason": "Resonates better with ad audience",
      "color_applied": "#FF6B6B"
    }
  ],
  "screenshot_original": "https://...",
  "screenshot_personalized": "https://..."
}
```

## Deployment

### Deploy Backend to Railway
```bash
cd backend
railway up
```

### Deploy Frontend to Vercel
```bash
cd frontend
vercel
```

See `railway.json` and `vercel.json` for configuration.

## Support

- **API Docs:** http://localhost:8000/docs
- **GitHub Issues:** Report issues with reproduction steps
- **Environment Variables:** Check backend/.env and frontend/.env
- **Logs:** Check terminal output for detailed error messages

---

**Happy Personalizing! 🚀**
