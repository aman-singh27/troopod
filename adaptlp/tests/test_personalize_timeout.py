import asyncio

from fastapi.testclient import TestClient

from app.main import app
from app.models import AdAnalysis, LPContent
import app.routes.personalize as personalize_route


def test_personalize_returns_504_when_ai_stage_times_out(monkeypatch):
    client = TestClient(app)

    async def slow_analyze_ad(*args, **kwargs):
        await asyncio.sleep(0.05)
        return AdAnalysis(
            headline="headline",
            offer="offer",
            cta_text="cta",
            tone="urgent",
            target_audience="audience",
            product_type="product",
            key_emotion="FOMO",
            color_palette=["#000000", "#111111", "#222222"],
        )

    async def fast_fetch_and_parse(*args, **kwargs):
        return LPContent(
            title="title",
            h1="h1",
            h2s=[],
            h3s=[],
            meta_description="desc",
            cta_buttons=["Click"],
            hero_subtext="subtext",
            raw_html="<html><head></head><body><h1>h1</h1></body></html>",
        )

    monkeypatch.setattr(personalize_route, "PERSONALIZE_AGENT_TIMEOUT_SECONDS", 0.01)
    monkeypatch.setattr(personalize_route.ad_analyzer, "analyze_ad", slow_analyze_ad)
    monkeypatch.setattr(personalize_route.lp_fetcher_agent, "fetch_and_parse", fast_fetch_and_parse)

    response = client.post(
        "/api/personalize",
        data={"lp_url": "https://example.com"},
        files={"ad_image": ("ad.png", b"fake-image-bytes", "image/png")},
    )

    assert response.status_code == 504
    assert "timed out" in response.json()["detail"].lower()