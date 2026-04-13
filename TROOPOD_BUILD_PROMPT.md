# TROOPOD AI LANDING PAGE PERSONALIZER — FULL BUILD SYSTEM PROMPT

> Paste this entire document into Cursor / Windsurf as your project-level system prompt.
> The build is structured as parallel agent tracks. Run Agent Track A and Agent Track B simultaneously, then merge at the integration step.

---

## PROJECT OVERVIEW

Build a full-stack web application called **AdaptLP** (internal name) — an AI-powered tool that takes an ad creative (image upload or URL) + a landing page URL and returns a personalized, CRO-optimized version of that landing page. The output is the **existing page modified in-place**, not a new page — headlines, subheadings, CTAs, and body copy are surgically updated to echo the ad's messaging while applying conversion rate optimization principles.

This is an internship assignment submission for **Troopod** — an AI-powered CRO and personalization platform for D2C brands. The product should feel like a native Troopod internal tool.

---

## TECH STACK

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | FastAPI (Python 3.11+) |
| AI | Google Gemini 1.5 Flash (free tier, multimodal) via `google-generativeai` SDK |
| Screenshot | Screenshotone API (primary) + Microlink API (fallback) |
| LP Fetching | `httpx` (async) + `BeautifulSoup4` |
| HTML Patching | `BeautifulSoup4` |
| Hosting | Vercel (frontend) + Railway (backend) |
| Env Management | `.env` files + `python-dotenv` |

---

## DESIGN SYSTEM — TROOPOD AESTHETIC

The UI must match Troopod's visual identity exactly. This is their tool, it should feel like their product.

```css
/* Core Design Tokens */
--bg-primary: #08080f;         /* near-black with slight purple tint */
--bg-secondary: #0f0f1a;       /* card backgrounds */
--bg-card: #13131f;            /* elevated cards */
--bg-card-hover: #1a1a2e;      /* hover state */
--accent-purple: #7c3aed;      /* primary purple - buttons, highlights */
--accent-purple-bright: #8b5cf6; /* brighter purple for gradients */
--accent-purple-light: #a78bfa; /* light purple for gradient text */
--accent-teal: #2dd4bf;        /* teal accent for gradient headlines */
--text-primary: #ffffff;
--text-secondary: #94a3b8;
--text-muted: #475569;
--border: rgba(124, 58, 237, 0.2);
--border-hover: rgba(124, 58, 237, 0.5);
--gradient-hero: linear-gradient(135deg, #2dd4bf, #7c3aed, #a78bfa);
--gradient-purple: linear-gradient(135deg, #7c3aed, #a78bfa);
--shadow-purple: 0 0 40px rgba(124, 58, 237, 0.15);
--radius-sm: 8px;
--radius-md: 16px;
--radius-lg: 24px;
--radius-pill: 9999px;

/* Font Stack */
font-family: 'Syne', 'Space Grotesk', sans-serif;  /* headlines */
font-family: 'DM Sans', sans-serif;                  /* body */
```

**Key UI Patterns to implement:**
- Dark cards with `border: 1px solid var(--border)` and subtle `box-shadow: var(--shadow-purple)`
- Pill-shaped primary CTA buttons filled with `--accent-purple`
- Pill-shaped secondary buttons with white border, transparent bg
- Gradient text on hero headlines (teal → purple → light purple left to right)
- Stat cards: large bold number, muted label below
- Status badges: small pill shapes with colored dot indicator
- Loading state: pulsing purple ring spinner
- All corners rounded, nothing sharp

---

## ARCHITECTURE — MULTI-AGENT PIPELINE

The backend runs **4 specialized agents in a coordinated pipeline**. Agents 1 and 2 run in **parallel** (using `asyncio.gather`). Agents 3 and 4 run sequentially after both complete.

```
USER INPUT
├── Ad Creative (image file OR URL)
└── Landing Page URL
         │
         ▼
┌─────────────────────────────────────┐
│     PARALLEL EXECUTION (asyncio)    │
│                                     │
│  AGENT 1: AD ANALYZER               │
│  - If image upload: base64 encode   │
│  - If URL: screenshot via API       │
│  - Feed image to Gemini Vision      │
│  - Extract: headline, offer, CTA,   │
│    tone, audience, color palette,   │
│    product/service type, emotion    │
│  Output: AdAnalysis JSON            │
│                                     │
│  AGENT 2: LP FETCHER                │
│  - httpx GET the landing page URL   │
│  - BeautifulSoup parse HTML         │
│  - Extract: title, h1, h2s, h3s,   │
│    meta description, CTA buttons,   │
│    hero subtext, nav items          │
│  - Store original HTML blob         │
│  Output: LPContent JSON + raw HTML  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  AGENT 3: CRO STRATEGIST            │
│  Inputs: AdAnalysis + LPContent     │
│  - Second Gemini call (text only)   │
│  - Generates modification plan:     │
│    specific text changes aligned    │
│    with ad messaging + CRO rules    │
│  Output: ModificationPlan JSON      │
│  Schema: [{ element, original,      │
│    replacement, cro_reason }]       │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  AGENT 4: HTML PATCHER              │
│  Inputs: raw HTML + ModificationPlan│
│  - For each modification in plan:   │
│    find element in BeautifulSoup    │
│    replace text content             │
│    skip if element not found        │
│  - Inject base href tag for assets  │
│  - Inject personalization banner    │
│  Output: Modified HTML string       │
└─────────────────────────────────────┘
         │
         ▼
RESPONSE TO FRONTEND
{
  modified_html: string,
  modifications: ModificationPlan[],
  ad_analysis: AdAnalysis,
  processing_time_ms: number
}
```

---

## COMPLETE FILE STRUCTURE

```
adaptlp/
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── AdInput.jsx           # Ad upload + URL tab switcher
│   │   │   ├── LPInput.jsx           # Landing page URL input
│   │   │   ├── ProcessingStatus.jsx  # 4-step agent status display
│   │   │   ├── ResultView.jsx        # Before/after iframe split view
│   │   │   ├── ModificationsPanel.jsx# Changes list with reasons
│   │   │   ├── AdAnalysisCard.jsx    # Shows what AI extracted from ad
│   │   │   └── Navbar.jsx            # Troopod-style top nav
│   │   ├── pages/
│   │   │   ├── Home.jsx              # Main input form page
│   │   │   └── Result.jsx            # Output/results page
│   │   ├── hooks/
│   │   │   └── usePersonalizer.js    # Main API call hook + state management
│   │   ├── utils/
│   │   │   └── api.js                # Axios instance + API helpers
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css                 # Tailwind + CSS variables
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app, CORS, routes
│   │   ├── config.py                 # Settings, env vars
│   │   ├── models.py                 # Pydantic request/response models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── ad_analyzer.py        # Agent 1: Gemini Vision analysis
│   │   │   ├── lp_fetcher.py         # Agent 2: LP HTML fetch + parse
│   │   │   ├── cro_strategist.py     # Agent 3: Gemini text modification plan
│   │   │   └── html_patcher.py       # Agent 4: BS4 HTML patching
│   │   ├── services/
│   │   │   ├── screenshot.py         # Screenshotone + Microlink fallback
│   │   │   └── gemini.py             # Gemini client wrapper
│   │   └── routes/
│   │       └── personalize.py        # POST /api/personalize endpoint
│   ├── requirements.txt
│   ├── .env.example
│   └── railway.json
│
├── tests/
│   ├── test_agents.py
│   ├── test_api.py
│   └── test_cases.md
│
└── README.md
```

---

## AGENT TRACK A — BACKEND (Build in parallel with Track B)

### A1. Project Setup

```
Create the backend directory structure exactly as shown above.

Install dependencies (requirements.txt):
fastapi==0.115.0
uvicorn[standard]==0.30.0
httpx==0.27.0
python-dotenv==1.0.0
google-generativeai==0.7.2
beautifulsoup4==4.12.3
lxml==5.2.2
pillow==10.4.0
pydantic==2.8.0
python-multipart==0.0.9
aiofiles==24.1.0
```

### A2. Environment Configuration (`config.py`)

```python
# Load from .env:
GEMINI_API_KEY=your_gemini_key
SCREENSHOTONE_API_KEY=your_screenshotone_key
MICROLINK_API_KEY=  # optional, microlink free works without key
ALLOWED_ORIGINS=http://localhost:5173,https://your-vercel-app.vercel.app
MAX_HTML_SIZE_KB=500
REQUEST_TIMEOUT_SECONDS=30
```

### A3. Pydantic Models (`models.py`)

Define these models exactly:

```python
class PersonalizeRequest(BaseModel):
    lp_url: HttpUrl
    ad_url: Optional[str] = None  # if URL input chosen
    # ad_image comes via multipart form, not JSON

class AdAnalysis(BaseModel):
    headline: str
    offer: str
    cta_text: str
    tone: str  # e.g. "urgent", "aspirational", "friendly", "professional"
    target_audience: str
    product_type: str
    key_emotion: str  # e.g. "FOMO", "trust", "excitement"
    color_palette: List[str]  # dominant hex colors from ad

class Modification(BaseModel):
    element_type: str  # "h1", "h2", "cta_button", "meta_description", "hero_subtext"
    original_text: str
    replacement_text: str
    cro_reason: str  # Why this change improves conversion

class PersonalizeResponse(BaseModel):
    modified_html: str
    modifications: List[Modification]
    ad_analysis: AdAnalysis
    original_url: str
    processing_time_ms: int
    screenshot_url: Optional[str] = None  # URL of ad screenshot if URL input
```

### A4. Screenshot Service (`services/screenshot.py`)

```python
# Implement get_screenshot(url: str) -> bytes
# 
# Primary: Screenshotone API
# GET https://api.screenshotone.com/take
# params: access_key, url, format=png, viewport_width=1280, 
#         viewport_height=800, full_page=false, delay=2
#
# Fallback (if screenshotone fails or returns non-200):
# GET https://api.microlink.io
# params: url={url}, screenshot=true, meta=false, embed=screenshot.url
# Note: microlink returns JSON, not image directly.
#   Parse response['data']['screenshot']['url'] then fetch that URL
#
# Return: raw PNG bytes
# Raise: ScreenshotError with message if both fail
```

### A5. Gemini Service (`services/gemini.py`)

```python
# Initialize Gemini client once at module level using GEMINI_API_KEY
# Use model: gemini-1.5-flash  (free tier, supports vision)
#
# Implement two functions:
#
# 1. analyze_ad_image(image_bytes: bytes) -> AdAnalysis
#    - Convert bytes to Gemini Part (inline_data, mime_type image/png)
#    - Prompt instructs Gemini to return ONLY valid JSON, no markdown, no preamble
#    - Response schema matches AdAnalysis model
#    - Parse JSON response safely with try/except
#    - If parse fails, retry once with stricter prompt
#
# 2. generate_modifications(ad_analysis: AdAnalysis, lp_content: dict) -> List[Modification]
#    - Text-only Gemini call
#    - lp_content contains: {title, h1, h2s, h3s, cta_buttons, hero_subtext, meta_desc}
#    - Prompt tells Gemini: you are a CRO expert. Given this ad analysis and LP content,
#      generate specific text changes to align the LP messaging with the ad.
#      Apply these CRO principles: message match, above-fold clarity, single primary CTA,
#      benefit-first headlines, urgency where appropriate.
#      Return ONLY a JSON array of modifications. No markdown. No explanation outside JSON.
#    - Validate each modification has all required fields
#    - Filter out any modification where replacement_text is empty or same as original
```

**CRITICAL GEMINI PROMPT for Agent 1 (Ad Analyzer):**

```
You are an expert ad creative analyst. Analyze this advertisement image and extract the following information.

Return ONLY a valid JSON object with exactly these fields, no markdown formatting, no explanation:
{
  "headline": "the main headline or key message of the ad",
  "offer": "the specific offer, discount, or value proposition",
  "cta_text": "the call-to-action text",
  "tone": "one of: urgent|aspirational|friendly|professional|playful|luxurious",
  "target_audience": "who this ad is targeting (1 short phrase)",
  "product_type": "what product or service category this is",
  "key_emotion": "primary emotion this ad triggers: FOMO|trust|excitement|aspiration|curiosity|relief",
  "color_palette": ["#hexcolor1", "#hexcolor2", "#hexcolor3"]
}

If you cannot determine a field, use a reasonable inference. Never return null.
```

**CRITICAL GEMINI PROMPT for Agent 3 (CRO Strategist):**

```
You are a world-class CRO (Conversion Rate Optimization) specialist.

AD ANALYSIS:
{ad_analysis_json}

CURRENT LANDING PAGE CONTENT:
{lp_content_json}

Your job: Generate specific text modifications to personalize this landing page to match the ad creative.

Rules:
1. Message match: The LP headline must echo the ad's core message so visitors feel continuity
2. Only modify text that exists in the LP content provided
3. Keep changes natural and professional — no keyword stuffing
4. Each replacement must be meaningfully different from the original
5. Maximum 8 modifications total
6. Focus on: h1, hero subtext, primary CTA button, meta description

Return ONLY a valid JSON array, no markdown, no preamble:
[
  {
    "element_type": "h1|h2|h3|cta_button|hero_subtext|meta_description",
    "original_text": "exact original text from LP content",
    "replacement_text": "your improved personalized version",
    "cro_reason": "one sentence explaining why this improves conversion"
  }
]
```

### A6. LP Fetcher Agent (`agents/lp_fetcher.py`)

```python
# async def fetch_and_parse(url: str) -> dict:
#
# 1. httpx.AsyncClient GET request with headers:
#    User-Agent: Mozilla/5.0 (compatible bot)
#    Accept: text/html
#    Timeout: 15 seconds
#
# 2. If status != 200, raise LPFetchError
#
# 3. If content-length > MAX_HTML_SIZE_KB * 1024, raise LPTooLargeError  
#
# 4. BeautifulSoup parse with 'lxml' parser
#
# 5. Extract and return:
#    {
#      "title": soup.title.string or "",
#      "h1": first h1 text or "",
#      "h2s": list of first 5 h2 texts,
#      "h3s": list of first 5 h3 texts,
#      "meta_description": meta[name=description] content or "",
#      "cta_buttons": list of button texts + a[class*=btn] texts (first 5),
#      "hero_subtext": first p tag inside header/hero section or first p after h1,
#      "raw_html": full HTML string
#    }
#
# 6. Add base href injection:
#    In raw_html, after <head>, inject: <base href="{url}">
#    This ensures all relative URLs (images, CSS) load correctly in iframe
```

### A7. HTML Patcher Agent (`agents/html_patcher.py`)

```python
# def apply_modifications(raw_html: str, modifications: List[Modification], original_url: str) -> str:
#
# 1. Parse HTML with BeautifulSoup
#
# 2. For each modification:
#    - Find matching element using element_type + original_text
#    - Strategy: search all tags of that type, find one whose .get_text(strip=True) 
#      matches original_text (exact or partial match >80%)
#    - If found: replace .string or .NavigableString
#    - If not found: log warning, skip (never crash)
#
# 3. Inject personalization banner at top of body:
#    A subtle floating banner: "✦ Personalized for this ad by AdaptLP"
#    Style: fixed bottom-right, small pill shape, purple bg, white text, z-index 9999
#    Make it dismissible with a small × button (inline JS)
#
# 4. Ensure <base href="{original_url}"> is in <head>
#
# 5. Return modified HTML as string
#
# IMPORTANT: Use try/except around EVERY element replacement.
#   If any single patch throws, skip it and continue — never fail the whole response.
```

### A8. Main Route (`routes/personalize.py`)

```python
# POST /api/personalize
# Content-Type: multipart/form-data
#
# Form fields:
#   lp_url: str (required)
#   ad_url: str (optional) 
#   ad_image: UploadFile (optional)
# Either ad_url or ad_image must be provided, not both required simultaneously
#
# Flow:
# 1. Validate: lp_url present + (ad_url OR ad_image present)
# 2. If ad_image: read bytes directly
#    If ad_url: call screenshot_service.get_screenshot(ad_url) -> bytes
# 3. asyncio.gather(
#      ad_analyzer.analyze_ad_image(image_bytes),  # Agent 1
#      lp_fetcher.fetch_and_parse(lp_url)           # Agent 2
#    ) — runs PARALLEL
# 4. cro_strategist.generate_modifications(ad_analysis, lp_content)  # Agent 3
# 5. html_patcher.apply_modifications(raw_html, modifications, lp_url)  # Agent 4
# 6. Return PersonalizeResponse
#
# Error handling:
#   - LPFetchError → 422 "Could not fetch the landing page. Check the URL."
#   - ScreenshotError → 422 "Could not capture ad screenshot. Try uploading the image instead."
#   - GeminiError → 500 "AI analysis failed. Please try again."
#   - All others → 500 with generic message
#
# Add: processing time tracking (time.time() at start, compute ms at end)
```

### A9. Main FastAPI App (`main.py`)

```python
# Setup:
# - CORS middleware with allowed origins from config
# - Include personalize router with prefix /api
# - Health check: GET /health -> {"status": "ok", "model": "gemini-1.5-flash"}
# - Request size limit: 10MB (for image uploads)
# - Uvicorn runner in __main__
```

---

## AGENT TRACK B — FRONTEND (Build in parallel with Track A)

### B1. Project Setup

```
Create React + Vite project in /frontend
Install dependencies:
- tailwindcss + autoprefixer + postcss
- axios
- react-router-dom
- @fontsource/syne
- @fontsource/dm-sans
- lucide-react (icons)
- react-hot-toast (notifications)
- framer-motion (animations)
```

### B2. Tailwind Config (`tailwind.config.js`)

```javascript
// Extend theme with Troopod design tokens:
// colors: {
//   'bg-primary': '#08080f',
//   'bg-secondary': '#0f0f1a', 
//   'bg-card': '#13131f',
//   'accent': '#7c3aed',
//   'accent-bright': '#8b5cf6',
//   'accent-light': '#a78bfa',
//   'accent-teal': '#2dd4bf',
// }
// Add custom animation: 'pulse-purple': pulsing glow effect
// Content: ['./src/**/*.{js,jsx}']
```

### B3. Global Styles (`index.css`)

```css
/* Import fonts: Syne (700, 800) + DM Sans (400, 500) from Google Fonts */
/* Set all CSS variables from design system */
/* Base: body { background: var(--bg-primary); color: var(--text-primary); font-family: 'DM Sans' } */
/* Custom scrollbar: thin, purple thumb */
/* Gradient text utility class: .gradient-text { background: var(--gradient-hero); -webkit-background-clip: text; color: transparent } */
/* Card base: .troopod-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); } */
/* Purple glow animation for loading spinner */
```

### B4. Navbar Component (`components/Navbar.jsx`)

```
Replicate Troopod's exact navbar:
- Left: Troopod logo SVG (the infinity-loop icon) + "troopod" wordmark in purple
- Right: hamburger menu icon (desktop: show nav links like Home, TrooCRO, TrooTech)
- Background: transparent with slight blur backdrop on scroll
- Fixed top, full width, z-index 50
- Use Syne font for brand name
```

### B5. Home Page (`pages/Home.jsx`)

```
Layout (single page, scrolls down):

SECTION 1 — HERO
- Small pill badge: "AI-Powered Growth & CRO Partner" (match Troopod style exactly)
- H1 with gradient text: "Personalize Your" [purple] "Landing Page with AI"
- Subtitle: "Transform any landing page to match your ad creative — powered by AI-driven CRO and message personalization."
- NO buttons here — CTA is the form below

SECTION 2 — INPUT FORM (the main UI)
Card with two columns on desktop, stacked on mobile:

LEFT COLUMN — Ad Creative Input:
  Tab switcher: [Upload Image] [From URL] 
  - Upload tab: drag-and-drop zone with dashed purple border
    Shows preview thumbnail after upload
    Accept: image/*, max 5MB
  - URL tab: text input with placeholder "https://your-ad-link.com"
    Info text: "We'll screenshot your ad automatically"
    
RIGHT COLUMN — Landing Page URL:
  Label: "Landing Page URL"
  Input: text field with placeholder "https://yourstore.com/product"
  Info text: "We'll fetch and analyze your existing page"

BELOW BOTH COLUMNS:
  Primary CTA button (full width, pill shape, purple fill):
  "Generate Personalized Page →"
  Loading state: show spinner + "Analyzing ad & fetching page..."

SECTION 3 — STATS ROW (below form)
  Three dark cards in a row:
  - "25% · Average Conversion Lift"
  - "2x · Faster Optimization"  
  - "5x · More Affordable"
  (Match Troopod's exact stat card design from screenshots)
```

### B6. Processing Status Component (`components/ProcessingStatus.jsx`)

```
Full-screen overlay or prominent card shown during API processing.
Shows 4 agent steps as a vertical timeline:

Step 1: "Analyzing Ad Creative"  [Agent 1 running]
Step 2: "Fetching Landing Page"  [Agent 2 running — parallel with step 1]
Step 3: "Generating CRO Strategy" [Agent 3 waiting → then active]
Step 4: "Applying Personalizations" [Agent 4 waiting → then active]

Visual states for each step:
- Pending: grey dot + muted text
- Running: pulsing purple dot + white text + spinner icon
- Complete: green checkmark + muted text
- Error: red X + error message

Since steps 1+2 run in parallel on backend, show both as "running" simultaneously.
Use a polling or estimated-time-based animation — the real status comes in one response,
so animate the steps with realistic timings:
- 0ms: Steps 1 + 2 both start (running)
- 3000ms: Steps 1 + 2 complete, Step 3 starts
- 5500ms: Step 3 completes, Step 4 starts
- 7000ms: Step 4 completes → response should arrive around here
Adjust timing if real response arrives faster (useEffect cleanup).
```

### B7. Result View (`pages/Result.jsx`)

```
Layout after successful API response:

TOP BAR:
  "← Back" button | "AdaptLP Result" | Processing time badge (e.g. "8.2s")

AD ANALYSIS CARD (collapsible):
  Show what AI extracted from the ad:
  - Headline, Offer, CTA, Tone, Target Audience, Key Emotion
  Purple badge for each field label, white text for value

MODIFICATIONS PANEL:
  Title: "X Changes Applied"
  List of each modification:
  - Element type badge (pill: "H1", "CTA", etc.)
  - Original text (strikethrough, muted)
  - Arrow →
  - New text (white, bold)
  - CRO reason (small italic teal text below)

PREVIEW SECTION (main feature — takes most screen space):
  Two-tab switcher: [Personalized Page] [Original Page]
  - Each tab shows the respective HTML in an IFRAME
  - iframe: width 100%, height 600px, border: 1px solid var(--border), border-radius var(--radius-md)
  - Sandbox attr: "allow-scripts allow-same-origin" (allow scripts so page renders properly)
  - For personalized: use blob URL from modified_html string
  - For original: use src={original_url}
  
  Below tabs: "Download Modified HTML" button (secondary style)
  onClick: create blob download of modified_html
```

### B8. API Hook (`hooks/usePersonalizer.js`)

```javascript
// Custom hook managing the entire personalization flow:
//
// State: { status: 'idle'|'processing'|'success'|'error', result: null, error: null }
//
// personalize(lpUrl, adInput, adInputType) async function:
// 1. Set status = 'processing'
// 2. Build FormData:
//    formData.append('lp_url', lpUrl)
//    if adInputType === 'file': formData.append('ad_image', adInput)
//    if adInputType === 'url': formData.append('ad_url', adInput)
// 3. POST to /api/personalize with axios
// 4. On success: set status = 'success', result = response.data
// 5. On error: set status = 'error', extract error message from response
// 6. Return { status, result, error, personalize, reset }
```

---

## INTEGRATION STEP — Connect Frontend + Backend

### Environment Variables

```bash
# frontend/.env
VITE_API_URL=http://localhost:8000

# frontend/.env.production  
VITE_API_URL=https://your-railway-app.railway.app
```

```bash
# backend/.env
GEMINI_API_KEY=your_key
SCREENSHOTONE_API_KEY=your_key
ALLOWED_ORIGINS=http://localhost:5173,https://your-vercel-app.vercel.app
```

### CORS Configuration

Backend must allow:
- Origin: Vercel frontend URL + localhost:5173
- Methods: GET, POST, OPTIONS
- Headers: Content-Type, Authorization
- `allow_credentials=True`

---

## ERROR HANDLING STRATEGY

### 1. Hallucinations (AI makes things up)
- Both Gemini calls use **strict JSON-only output** prompts — no prose allowed
- Response validated against Pydantic models before use
- If JSON parse fails → retry once with `"Return ONLY raw JSON, absolutely no other text"`
- If second parse fails → return partial result with empty modifications (LP still renders)
- `replacement_text` max length: 200 chars enforced — longer ones are truncated

### 2. Broken UI in Preview
- `<base href>` injected into fetched HTML so relative assets (CSS/images) load correctly
- iframe sandboxed but allows scripts (`allow-scripts allow-same-origin`)
- If iframe shows blank: fallback tab "View Source" shows syntax-highlighted HTML
- CSP conflicts: if page refuses to load in iframe due to X-Frame-Options, show message: "This page blocks iframe embedding. Download the HTML to view locally."

### 3. Inconsistent Outputs
- Gemini temperature: `0.3` (low, deterministic)
- Structured JSON schema in prompt (not `response_mime_type` — free tier may not support it)
- Modifications filtered: skip any where `replacement_text == original_text`
- Modifications filtered: skip any where `replacement_text` is empty or < 5 chars
- Max 8 modifications enforced at the patcher level too

### 4. Random / Irrelevant Changes
- CRO Strategist prompt explicitly says: "Only modify text that exists in the LP content provided"
- Each modification must include a `cro_reason` — this forces the AI to justify changes
- LP content passed to Agent 3 is limited to extracted text only (not raw HTML) — reduces hallucinated selectors

### 5. LP Fetch Failures
- Timeout: 15 seconds — if LP doesn't respond, clear error message
- Redirect following: enabled (httpx follow_redirects=True)
- Large pages: skip if HTML > 500KB, tell user

### 6. Screenshot API Failures
- Primary: Screenshotone → Fallback: Microlink (automatic, transparent to user)
- If both fail: return error "Could not capture ad screenshot. Please upload the image directly."

---

## TESTING CASES

Create `tests/test_cases.md` with manual test scenarios to verify before submission:

### Test Case 1 — Happy Path (Image Upload)
```
Input:
  ad_image: a product ad image (any brand — shoes, skincare, electronics)
  lp_url: https://troopod.io

Expected:
  - Response status 200
  - modifications array has 3-8 items
  - modified_html contains <base href="https://troopod.io">
  - At least one modification has element_type = "h1"
  - personalization banner present in modified_html
  - Preview iframe renders the Troopod page with modified headlines
```

### Test Case 2 — Happy Path (Ad URL)
```
Input:
  ad_url: any live product page URL (used as ad creative)
  lp_url: https://troopod.io

Expected:
  - Backend successfully screenshots the ad_url
  - Same result structure as Test Case 1
  - No error about screenshot failure
```

### Test Case 3 — Invalid LP URL
```
Input:
  ad_image: [valid image]
  lp_url: https://this-website-does-not-exist-xyz123.com

Expected:
  - 422 response
  - Error message: "Could not fetch the landing page. Check the URL."
  - Frontend shows error state, not crash
```

### Test Case 4 — Large Image Upload
```
Input:
  ad_image: image > 5MB
  lp_url: any valid URL

Expected:
  - Frontend rejects before upload with message "Image must be under 5MB"
  - No API call made
```

### Test Case 5 — Neither Ad Input Provided
```
Input:
  lp_url: https://troopod.io
  (no ad_image, no ad_url)

Expected:
  - Frontend form validation prevents submission
  - Error: "Please provide an ad image or URL"
```

### Test Case 6 — X-Frame-Options Block
```
Input:
  ad_image: [valid image]
  lp_url: https://google.com  (blocks iframes)

Expected:
  - API returns modified HTML successfully  
  - Frontend iframe shows blank/blocked
  - Fallback message shown: "This page blocks preview. Download the HTML to view locally."
  - Download button still works
```

### Test Case 7 — Gemini Rate Limit (Free Tier)
```
Simulate by sending 16+ requests within 1 minute.

Expected:
  - Backend catches 429 from Gemini
  - User sees: "AI service is busy. Please wait 30 seconds and try again."
  - No crash, no 500 with stack trace
```

### Test Case 8 — Mobile Responsive
```
Resize browser to 375px width (iPhone SE)

Expected:
  - Input form stacks vertically
  - Ad input + LP input in single column
  - Buttons full width
  - Result page: modifications panel + iframe scrollable
  - No horizontal overflow
```

### Automated Tests (`tests/test_agents.py`)

```python
# Write pytest tests for:
#
# 1. test_lp_fetcher_valid_url() 
#    - Fetch https://troopod.io, assert h1 is not empty, raw_html is not empty
#
# 2. test_lp_fetcher_invalid_url()
#    - Fetch invalid URL, assert LPFetchError raised
#
# 3. test_html_patcher_applies_modification()
#    - Create minimal HTML: <html><body><h1>Original</h1></body></html>
#    - Apply modification: {element_type: "h1", original: "Original", replacement: "New"}
#    - Assert "New" in result, "Original" not in result
#
# 4. test_html_patcher_skips_missing_element()
#    - Create HTML without h2
#    - Apply modification targeting h2
#    - Assert no exception, original HTML unchanged for other elements
#
# 5. test_html_patcher_injects_base_href()
#    - Apply any modification to minimal HTML
#    - Assert '<base href=' in result
#
# 6. test_gemini_ad_analysis_returns_valid_schema() [integration, skipped if no key]
#    - Load test image from tests/fixtures/sample_ad.png
#    - Call analyze_ad_image()
#    - Assert result is valid AdAnalysis (all fields present, non-empty)
```

---

## DEPLOYMENT GUIDE

### Backend → Railway

```bash
# railway.json (in /backend):
{
  "build": { "builder": "NIXPACKS" },
  "deploy": { 
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}

# Set environment variables in Railway dashboard:
# GEMINI_API_KEY, SCREENSHOTONE_API_KEY, ALLOWED_ORIGINS
```

### Frontend → Vercel

```bash
# vercel.json (in /frontend):
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}

# Set in Vercel dashboard:
# VITE_API_URL = https://your-railway-app.railway.app
```

### Post-Deploy Checklist
- [ ] `GET /health` returns 200 from Railway URL
- [ ] CORS allows Vercel frontend origin
- [ ] Test Case 1 passes on production URL
- [ ] Test Case 3 shows correct error (not 500)
- [ ] Gemini key active and not expired
- [ ] Screenshotone key active

---

## IMPLEMENTATION NOTES & ASSUMPTIONS

1. **Troopod's own site** is used as the demo LP since it's a Next.js SSR site that renders well with simple httpx fetch.

2. **Ad creative**: For demo purposes, any product ad image works. The assignment doesn't specify a particular ad format.

3. **Personalization banner**: The small "Personalized by AdaptLP" badge injected into the page makes it visually clear the page has been modified, which is important for the demo evaluator.

4. **SPA limitation**: Sites built purely in React/Vue/Angular won't render full content with `httpx` alone (you get an empty shell HTML). This is a **known and documented limitation** — mention it in the Google Doc brief. For the demo, use SSR/static sites like Shopify stores, WordPress, or Troopod.io itself.

5. **Free tier limits**:
   - Gemini 1.5 Flash: 15 RPM, 1M tokens/day — sufficient for demo
   - Screenshotone: 100 screenshots/month free
   - Microlink: 50 req/day free
   - Railway free tier: 500 hours/month — sufficient

6. **Image upload size**: 5MB frontend limit, 10MB backend limit. Gemini handles up to ~4MB inline images.

---

## GOOGLE DOC BRIEF — KEY POINTS TO INCLUDE

Write the explanation doc to cover:

**System Flow:** Reference the 4-agent pipeline above. Draw a simple ASCII or diagram version.

**Key Components:**
- Ad Analyzer: Gemini Vision multimodal call
- LP Fetcher: httpx + BeautifulSoup  
- CRO Strategist: Gemini text call with CRO-specialized prompt
- HTML Patcher: BeautifulSoup surgical text replacement

**Handling Random Changes:** Strict JSON schema in prompt + Pydantic validation + `cro_reason` field forces justification

**Handling Broken UI:** base href injection + iframe sandbox + fallback download button + X-Frame-Options detection

**Hallucinations:** Temperature 0.3 + JSON-only output instruction + retry logic + empty/same-text filtering

**Inconsistent Outputs:** Deterministic temperature + max modification count + source-text matching (only change what's in the extracted LP content)
