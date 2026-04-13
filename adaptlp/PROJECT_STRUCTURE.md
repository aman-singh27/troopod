```
adaptlp/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Config loading
│   │   ├── config.py                # Environment vars validation
│   │   ├── models.py                # Pydantic schemas
│   │   ├── main.py                  # FastAPI app + CORS + routes
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── ad_analyzer.py       # Agent 1: Gemini Vision analysis
│   │   │   ├── lp_fetcher.py        # Agent 2: LP HTML fetch + parse
│   │   │   ├── cro_strategist.py    # Agent 3: Gemini text modifications
│   │   │   └── html_patcher.py      # Agent 4: BeautifulSoup patching
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── gemini.py            # Gemini client wrapper + prompts
│   │   │   └── screenshot.py        # Screenshotone + Microlink fallback
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── personalize.py       # POST /api/personalize endpoint
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Local environment (add GEMINI_API_KEY)
│   ├── .env.example                 # Environment template
│   ├── railway.json                 # Railway deployment config
│   └── pytest.ini                   # pytest configuration
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Troopod brand navbar
│   │   │   ├── AdInput.jsx          # Upload/URL ad input (tabbed)
│   │   │   ├── LPInput.jsx          # Landing page URL input
│   │   │   ├── ProcessingStatus.jsx # 4-step timeline overlay
│   │   │   ├── ModificationsPanel.jsx # Changes list with CRO reasons
│   │   │   └── AdAnalysisCard.jsx   # Ad analysis + color palette
│   │   ├── pages/
│   │   │   ├── Home.jsx             # Main input form page
│   │   │   └── Result.jsx           # Results + preview page
│   │   ├── hooks/
│   │   │   └── usePersonalizer.js   # API + state management hook
│   │   ├── utils/
│   │   │   └── api.js               # Axios + personalizeAPI
│   │   ├── App.jsx                  # Route orchestration
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Tailwind + CSS variables
│   ├── public/                      # Static assets
│   ├── package.json                 # Node dependencies
│   ├── vite.config.js               # Vite configuration
│   ├── tailwind.config.js           # Tailwind + Troopod tokens
│   ├── postcss.config.js            # PostCSS + autoprefixer
│   ├── .eslintrc.json               # ESLint configuration
│   ├── index.html                   # HTML entry
│   ├── .env                         # Local env (http://localhost:8000)
│   ├── .env.production              # Production env (Railway URL)
│   └── vercel.json                  # Vercel deployment config
│
├── tests/
│   ├── test_agents.py               # pytest for backend agents
│   └── test_cases.md                # Manual test scenarios (8 cases)
│
├── README.md                        # Project overview + setup guide
├── IMPLEMENTATION_SUMMARY.md        # Full implementation details
└── PROJECT_STRUCTURE.md             # This file
```

## What Was Built

### ✅ Complete Backend (FastAPI)
- 4-agent pipeline (parallel agents 1-2, sequential agents 3-4)
- Gemini Vision API integration for ad analysis
- Gemini text API for CRO strategy generation
- httpx + BeautifulSoup for LP fetching/parsing
- Screenshot service with Screenshotone + Microlink fallback
- HTML surgical patching with personalization banner injection
- Comprehensive error handling with HTTP status codes
- CORS configuration for frontend
- Deployment-ready config (Railway)

### ✅ Complete Frontend (React + Vite + Tailwind)
- Responsive design (mobile-first)
- Troopod brand aesthetic (dark theme, purple accents, gradient text)
- Ad input component (upload image or URL)
- LP input component
- Processing status overlay (4-step timeline)
- Results page with before/after iframe preview
- Modifications panel showing changes + CRO reasoning
- Ad analysis card showing extracted data
- HTML download button
- Error handling + toast notifications
- Fully styled with Tailwind + CSS variables
- ESLint configured for code quality

### ✅ Testing & Documentation
- pytest unit tests for HTML patcher agent
- 8 manual test cases (happy path, errors, edge cases, mobile)
- README with setup, API docs, deployment guide
- Implementation summary with architecture highlights
- Environment configuration templates
- Deployment configs for Railway (backend) + Vercel (frontend)

## Key Features

✅ **AI-Powered Analysis** - Google Gemini 1.5 Flash (multimodal)
✅ **Parallel Processing** - asyncio.gather() for agents 1 & 2
✅ **Smart Fallbacks** - Screenshot failures auto-fallover to Microlink
✅ **HTML Safety** - Graceful element skip, base href injection, iframe sandbox
✅ **Error Resilience** - Clear error messages, no crashes, 422/500 status codes
✅ **Responsive UI** - Works on mobile (375px) to desktop
✅ **Production Ready** - Deployment configs, tests, documentation

## To Get Started

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Add your GEMINI_API_KEY to .env
python -m uvicorn app.main:app --reload
# API will be at http://localhost:8000
```

### 2. Frontend
```bash
cd ../frontend
npm install
npm run dev
# UI will open at http://localhost:5173
```

### 3. Test
- Upload an ad image or provide ad URL
- Enter a landing page URL (e.g., https://troopod.io)
- Click "Generate Personalized Page"
- Wait 8-10 seconds for processing
- View personalized page in the before/after preview
- Download modified HTML if desired

## Deployment

**Backend** → Railway:
- Push code with `railway.json` config
- Set `GEMINI_API_KEY`, `SCREENSHOTONE_API_KEY` environment variables

**Frontend** → Vercel:
- Push code with `vercel.json` config
- Set `VITE_API_URL` environment variable to Railway URL

## Tech Stack

- **Backend**: FastAPI, Python 3.11+, Pydantic, BeautifulSoup4, httpx
- **Frontend**: React 18, Vite, Tailwind CSS, axios, lucide-react
- **AI**: Google Gemini 1.5 Flash
- **Services**: Screenshotone, Microlink (screenshot), Railway (hosting)
