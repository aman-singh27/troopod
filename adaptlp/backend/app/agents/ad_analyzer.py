from app.services.gemini import analyze_ad_image

async def analyze_ad(image_bytes: bytes, api_key_override: str | None = None):
    """Agent 1: Analyze ad creative"""
    return await analyze_ad_image(image_bytes, api_key_override=api_key_override)
