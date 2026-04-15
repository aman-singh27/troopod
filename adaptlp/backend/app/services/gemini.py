import asyncio
import json
import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_FALLBACK_MODELS
from app.models import AdAnalysis, Modification
from typing import List, Iterable

genai.configure(api_key=GEMINI_API_KEY)

class GeminiError(Exception):
    pass


def _build_modification_prompt(ad_analysis: AdAnalysis, lp_content: dict) -> str:
    return f"""You are a world-class CRO (Conversion Rate Optimization) specialist.

AD ANALYSIS:
{json.dumps(ad_analysis.model_dump(), indent=2)}

CURRENT LANDING PAGE CONTENT:
{json.dumps(lp_content, indent=2)}

Your job: generate text-only landing page improvements that preserve the page structure while strengthening message match.

Rules:
1. The H1 MUST directly echo the ad's core promise or offer so the user immediately feels continuity.
2. H2 and H3 changes are optional and should only be made when they reinforce the same message.
3. CTA button text MUST align with the ad CTA and stay short, specific, and action-oriented.
4. Hero subtext should support the H1 with clarity, urgency, trust, or specificity.
5. Meta description should improve relevance, but never introduce claims that are not supported by the ad.
6. Only modify text that exists in the LP content provided.
7. Keep changes natural and professional - no keyword stuffing.
8. Each replacement must be meaningfully different from the original.
9. Maximum 8 modifications total.
10. Favor message match over clever wording.

Return ONLY a valid JSON array, no markdown, no preamble:
[\n  {{\n    "element_type": "h1|h2|h3|cta_button|hero_subtext|meta_description",\n    "original_text": "exact original text from LP content",\n    "replacement_text": "your improved personalized version",\n    "cro_reason": "one sentence explaining why this improves conversion"\n  }}\n]"""


def _resolve_api_key(api_key_override: str | None) -> str:
    """Use user-provided key when present, otherwise fallback to server key."""
    if api_key_override and api_key_override.strip():
        return api_key_override.strip()
    return GEMINI_API_KEY


def _model_candidates() -> list[str]:
    """Return unique model candidates in priority order."""
    ordered: list[str] = [GEMINI_MODEL, *GEMINI_FALLBACK_MODELS]
    unique: list[str] = []
    for model in ordered:
        if model and model not in unique:
            unique.append(model)
    return unique


def _generate_with_fallback(parts: Iterable, api_key_override: str | None = None):
    resolved_api_key = _resolve_api_key(api_key_override)
    if not resolved_api_key:
        raise GeminiError("Gemini API key is missing. Provide a valid key.")

    genai.configure(api_key=resolved_api_key)
    errors: list[str] = []
    for model_name in _model_candidates():
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(parts)
        except Exception as exc:
            errors.append(f"{model_name}: {exc}")

    raise GeminiError("All configured Gemini models failed. " + " | ".join(errors))

async def analyze_ad_image(image_bytes: bytes, api_key_override: str | None = None) -> AdAnalysis:
    """Analyze ad image using Gemini Vision API"""
    try:
        prompt = """You are an expert ad creative analyst. Analyze this advertisement image and extract the following information.

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

If you cannot determine a field, use a reasonable inference. Never return null."""

        response = await asyncio.to_thread(
            _generate_with_fallback,
            [
                {"mime_type": "image/png", "data": image_bytes},
                prompt,
            ],
            api_key_override,
        )
        
        # Extract JSON from response
        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        data = json.loads(response_text)
        return AdAnalysis(**data)
    
    except json.JSONDecodeError as e:
        raise GeminiError(f"Failed to parse Gemini response as JSON: {e}")
    except Exception as e:
        raise GeminiError(f"Gemini Vision analysis failed: {str(e)}")

async def generate_modifications(
    ad_analysis: AdAnalysis,
    lp_content: dict,
    api_key_override: str | None = None,
) -> List[Modification]:
    """Generate CRO modification strategy using Gemini"""
    try:
        prompt = _build_modification_prompt(ad_analysis, lp_content)

        response = await asyncio.to_thread(
            _generate_with_fallback,
            prompt,
            api_key_override,
        )

        # Extract JSON from response
        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()

        data = json.loads(response_text)
        modifications = [Modification(**mod) for mod in data]

        # Filter: skip if replacement same as original or too short
        modifications = [
            m
            for m in modifications
            if m.replacement_text.strip() and m.replacement_text != m.original_text
        ]

        return modifications[:8]  # Max 8 modifications

    except json.JSONDecodeError as e:
        raise GeminiError(f"Failed to parse modifications response as JSON: {e}")
    except GeminiError:
        raise
    except Exception as e:
        raise GeminiError(f"CRO strategy generation failed: {str(e)}")
