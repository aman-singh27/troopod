import pytest
from bs4 import BeautifulSoup
from app.agents.lp_fetcher import LPFetchError
from app.agents.html_patcher import apply_modifications
from app.models import Modification

def test_html_patcher_applies_h1_modification():
    """Test that HTML patcher correctly modifies h1 tag"""
    html = """
    <html>
        <head></head>
        <body>
            <h1>Original Headline</h1>
            <p>Content here</p>
        </body>
    </html>
    """
    
    modifications = [
        Modification(
            element_type="h1",
            original_text="Original Headline",
            replacement_text="New Personalized Headline",
            cro_reason="Better aligns with ad message"
        )
    ]
    
    result = apply_modifications(html, modifications, "https://example.com")
    assert "New Personalized Headline" in result
    assert "Original Headline" not in result


def test_html_patcher_skips_missing_element():
    """Test that patcher skips modifications for non-existent elements"""
    html = """
    <html>
        <head></head>
        <body>
            <h1>Original</h1>
        </body>
    </html>
    """
    
    modifications = [
        Modification(
            element_type="h2",
            original_text="Non-existent h2",
            replacement_text="Should not crash",
            cro_reason="Safety test"
        )
    ]
    
    # Should not raise exception
    result = apply_modifications(html, modifications, "https://example.com")
    assert "Original" in result


def test_html_patcher_injects_base_href():
    """Test that patcher injects base href"""
    html = "<html><head></head><body><p>Test</p></body></html>"
    modifications = []
    
    result = apply_modifications(html, modifications, "https://example.com")
    assert 'base href="https://example.com"' in result


def test_html_patcher_injects_banner():
    """Test that personalization banner is injected"""
    html = "<html><head></head><body><p>Test</p></body></html>"
    modifications = []
    
    result = apply_modifications(html, modifications, "https://example.com")
    assert "Personalized for this ad by AdaptLP" in result
