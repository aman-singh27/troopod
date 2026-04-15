# pyright: reportMissingImports=false

from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
  sys.path.insert(0, str(BACKEND_ROOT))

from bs4 import BeautifulSoup

from app.agents.html_patcher import apply_modifications
from app.agents.lp_fetcher import _extract_hero_subtext
from app.models import AdAnalysis, Modification
from app.services.gemini import _build_modification_prompt


def test_html_patcher_handles_nested_heading_text():
    html = """
    <html>
      <head></head>
      <body>
        <h1><span>Original <em>Headline</em></span></h1>
      </body>
    </html>
    """
    modifications = [
        Modification(
            element_type="h1",
            original_text="Original Headline",
            replacement_text="New Personalized Headline",
            cro_reason="Message match",
        )
    ]

    result = apply_modifications(html, modifications, "https://example.com")
    assert "New Personalized Headline" in result
    assert "Original Headline" not in result


def test_html_patcher_injects_js_fallback_when_no_bs4_match():
    html = """
    <html>
      <head></head>
      <body>
        <div class="hero-copy">Welcome</div>
      </body>
    </html>
    """
    modifications = [
        Modification(
            element_type="cta_button",
            original_text="Join now",
            replacement_text="Start free trial",
            cro_reason="CTA alignment",
        )
    ]

    result = apply_modifications(html, modifications, "https://example.com")
    assert 'id="adaptlp-patches"' in result
    assert "Start free trial" in result


def test_extract_hero_subtext_from_header_first():
    soup = BeautifulSoup(
        """
        <html>
          <body>
            <header><p>Header hero description goes here</p></header>
            <h1>Main Headline</h1>
          </body>
        </html>
        """,
        "lxml",
    )
    h1_tag = soup.find("h1")

    assert _extract_hero_subtext(soup, h1_tag) == "Header hero description goes here"


def test_build_modification_prompt_contains_directives():
    ad_analysis = AdAnalysis(
        headline="Save 30% today",
        offer="30% off",
        cta_text="Shop now",
        tone="urgent",
        target_audience="deal seekers",
        product_type="ecommerce",
        key_emotion="FOMO",
        color_palette=["#111111", "#222222", "#333333"],
    )
    lp_content = {
        "title": "Example",
        "h1": "Original headline",
        "h2s": [],
        "h3s": [],
        "meta_description": "Original desc",
        "cta_buttons": ["Learn more"],
        "hero_subtext": "Original subtext",
    }

    prompt = _build_modification_prompt(ad_analysis, lp_content)
    assert "H1 MUST directly echo" in prompt
    assert "CTA button text MUST align" in prompt
    assert "message match" in prompt.lower()
