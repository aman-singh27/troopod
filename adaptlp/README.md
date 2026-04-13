# AdaptLP - AI Landing Page Personalizer

A full-stack web application that personalizes landing pages by analyzing ad creatives using AI.

## Project Overview

**AdaptLP** is an AI-powered tool that takes an ad creative (image or URL) + a landing page URL and returns a personalized, CRO-optimized version of that landing page. The output is the existing page modified in-place, not a new page.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | FastAPI (Python 3.11+) |
| AI | Google Gemini 1.5 Flash (multimodal) |
| Screenshot | Screenshotone API + Microlink fallback |
| LP Fetching | httpx + BeautifulSoup4 |
| Hosting | Vercel (frontend) + Railway (backend) |

## Architecture

The backend runs 4 specialized agents in a coordinated pipeline:

```
USER INPUT (Ad Creative + LP URL)
    ↓
[PARALLEL] Agent 1: Ad Analyzer + Agent 2: LP Fetcher
    ↓
Agent 3: CRO Strategist
    ↓
Agent 4: HTML Patcher
    ↓
PERSONALIZED HTML + MODIFICATIONS + ANALYSIS
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
python -m uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will open at `http://localhost:5173`

## API Endpoint

```
POST /api/personalize
Content-Type: multipart/form-data

Fields:
- lp_url (required): Landing page URL to personalize
- ad_url (optional): URL of ad creative (screenshot auto-captured)
- ad_image (optional): Upload ad image file directly

Response:
{
  "modified_html": "...",
  "modifications": [...],
  "ad_analysis": {...},
  "original_url": "...",
  "processing_time_ms": 8234,
  "screenshot_url": "..."
}
```

## Deployment

### Backend → Railway

1. Create Railway project
2. Set environment variables in Railway dashboard
3. Deploy from Git

### Frontend → Vercel

1. Create Vercel project
2. Set `VITE_API_URL` environment variable
3. Deploy from Git

## Testing

```bash
# Run backend tests
cd backend
pytest tests/

# Frontend - manual testing via UI for now
```

## Design System

Troopod brand aesthetic:
- Dark backgrounds: `#08080f`, `#0f0f1a`, `#13131f`
- Primary accent: `#7c3aed` (purple)
- Teal accent: `#2dd4bf`
- Gradient text, pill buttons, shadow effects

## Error Handling

- **LP Fetch Failures**: Clear error messages + timeout protection
- **Screenshot API Failures**: Automatic fallback from Screenshotone to Microlink
- **Gemini Hallucinations**: JSON-only output + strict parsing + validation
- **HTML Rendering**: Base href injection + iframe sandbox + fallback download

## Known Limitations

- SPA-only sites (React/Vue/Angular) won't render full content without JavaScript execution
- Large pages (>500KB) are rejected to prevent timeout
- Rate limits: Gemini 15 RPM, Screenshotone 100/month free

## Features

✅ AI-powered ad analysis (vision + text understanding)
✅ Parallel agent pipeline for fast processing
✅ CRO-optimized text modifications
✅ HTML surgical patching with BeautifulSoup
✅ Browser-based preview with iframe
✅ Responsive mobile UI
✅ Error handling & fallbacks
✅ Deployment-ready config

## Contributing

This is an internship submission for Troopod. For changes, please follow the skill guidelines:
- Use Test-Driven Development for new features
- Follow React best practices for frontend code
- Validate code with lint before committing
