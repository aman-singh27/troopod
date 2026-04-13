from app.services.gemini import generate_modifications
from app.models import AdAnalysis

async def generate_strategy(
    ad_analysis: AdAnalysis,
    lp_content: dict,
    api_key_override: str | None = None,
):
    """Agent 3: Generate CRO modification strategy"""
    return await generate_modifications(ad_analysis, lp_content, api_key_override=api_key_override)
