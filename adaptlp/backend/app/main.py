from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS, GEMINI_MODEL
from app.routes.personalize import router as personalize_router

app = FastAPI(title="AdaptLP API")

_LOCAL_DEV_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
resolved_origins = list(dict.fromkeys([*ALLOWED_ORIGINS, *_LOCAL_DEV_ORIGINS]))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=resolved_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(personalize_router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": GEMINI_MODEL}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
