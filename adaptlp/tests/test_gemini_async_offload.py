import types

import pytest

from app.services import gemini
from app.models import AdAnalysis


@pytest.mark.asyncio
async def test_analyze_ad_image_uses_asyncio_to_thread(monkeypatch):
    called = {"value": False}

    async def fake_to_thread(func, *args, **kwargs):
        called["value"] = True
        return types.SimpleNamespace(
            text='{"headline":"h","offer":"o","cta_text":"c","tone":"urgent","target_audience":"a","product_type":"p","key_emotion":"FOMO","color_palette":["#000000","#111111","#222222"]}'
        )

    monkeypatch.setattr(gemini.asyncio, "to_thread", fake_to_thread)

    result = await gemini.analyze_ad_image(b"image-bytes")
    assert called["value"] is True
    assert result.headline == "h"


@pytest.mark.asyncio
async def test_generate_modifications_uses_asyncio_to_thread(monkeypatch):
    called = {"value": False}

    async def fake_to_thread(func, *args, **kwargs):
        called["value"] = True
        return types.SimpleNamespace(
            text='[{"element_type":"h1","original_text":"old","replacement_text":"new","cro_reason":"reason"}]'
        )

    monkeypatch.setattr(gemini.asyncio, "to_thread", fake_to_thread)

    ad_analysis = AdAnalysis(
        headline="h",
        offer="o",
        cta_text="c",
        tone="urgent",
        target_audience="audience",
        product_type="product",
        key_emotion="FOMO",
        color_palette=["#000000", "#111111", "#222222"],
    )

    mods = await gemini.generate_modifications(ad_analysis, {"h1": "old"})
    assert called["value"] is True
    assert len(mods) == 1
    assert mods[0].replacement_text == "new"
