from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class AdAnalysis(BaseModel):
    headline: str
    offer: str
    cta_text: str
    tone: str
    target_audience: str
    product_type: str
    key_emotion: str
    color_palette: List[str]

class Modification(BaseModel):
    element_type: str
    original_text: str
    replacement_text: str
    cro_reason: str

class PersonalizeRequest(BaseModel):
    lp_url: HttpUrl

class PersonalizeResponse(BaseModel):
    modified_html: str
    modifications: List[Modification]
    ad_analysis: AdAnalysis
    original_url: str
    processing_time_ms: int
    screenshot_url: Optional[str] = None

class LPContent(BaseModel):
    title: str
    h1: str
    h2s: List[str]
    h3s: List[str]
    meta_description: str
    cta_buttons: List[str]
    hero_subtext: str
    raw_html: str
