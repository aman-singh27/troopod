import time
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models import PersonalizeResponse
from app.agents import ad_analyzer, lp_fetcher as lp_fetcher_agent, cro_strategist
from app.agents.html_patcher import apply_modifications
from app.services.screenshot import get_screenshot, ScreenshotError
from app.services.gemini import GeminiError
from app.agents.lp_fetcher import LPFetchError

router = APIRouter(prefix="/api", tags=["personalize"])


def _map_gemini_error(stage: str, error_text: str) -> HTTPException:
    """Convert provider-specific Gemini failures into stable API responses."""
    lowered = error_text.lower()

    if "quota" in lowered or "429" in lowered or "rate limit" in lowered:
        return HTTPException(
            status_code=429,
            detail=(
                "AI quota exceeded for the configured Gemini API key. "
                "Enable billing or increase quota, then retry."
            ),
        )

    if "api_key" in lowered or "authentication" in lowered or "permission" in lowered:
        return HTTPException(
            status_code=401,
            detail="Gemini API authentication failed. Check GEMINI_API_KEY and project permissions.",
        )

    return HTTPException(status_code=500, detail=f"{stage} failed: {error_text}")

@router.post("/personalize", response_model=PersonalizeResponse)
async def personalize(
    lp_url: str = Form(...),
    ad_url: str = Form(None),
    ad_image: UploadFile = File(None),
    gemini_api_key: str = Form(None),
):
    """Main personalization endpoint"""
    start_time = time.time()
    
    try:
        # Validate inputs
        if not lp_url:
            raise HTTPException(status_code=422, detail="lp_url is required")
        
        if not ad_url and not ad_image:
            raise HTTPException(status_code=422, detail="Either ad_url or ad_image is required")
        
        # Get ad image bytes
        screenshot_url = None
        if ad_image:
            image_bytes = await ad_image.read()
        else:
            try:
                image_bytes = await get_screenshot(ad_url)
                screenshot_url = ad_url
            except ScreenshotError as e:
                raise HTTPException(status_code=422, detail=str(e))
        
        # Run agents in parallel (1 & 2)
        try:
            ad_analysis, lp_content = await asyncio.gather(
                ad_analyzer.analyze_ad(image_bytes, api_key_override=gemini_api_key),
                lp_fetcher_agent.fetch_and_parse(lp_url)
            )
        except GeminiError as e:
            raise _map_gemini_error("AI analysis", str(e))
        except LPFetchError as e:
            raise HTTPException(status_code=422, detail=f"Could not fetch landing page: {str(e)}")
        
        # Agent 3: Generate modifications
        try:
            lp_dict = {
                "title": lp_content.title,
                "h1": lp_content.h1,
                "h2s": lp_content.h2s,
                "h3s": lp_content.h3s,
                "meta_description": lp_content.meta_description,
                "cta_buttons": lp_content.cta_buttons,
                "hero_subtext": lp_content.hero_subtext
            }
            modifications = await cro_strategist.generate_strategy(
                ad_analysis,
                lp_dict,
                api_key_override=gemini_api_key,
            )
        except GeminiError as e:
            raise _map_gemini_error("CRO strategy", str(e))
        
        # Agent 4: Apply modifications
        modified_html = apply_modifications(lp_content.raw_html, modifications, str(lp_url))
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return PersonalizeResponse(
            modified_html=modified_html,
            modifications=modifications,
            ad_analysis=ad_analysis,
            original_url=str(lp_url),
            processing_time_ms=processing_time_ms,
            screenshot_url=screenshot_url
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
