import importlib

import app.config as config


def test_default_model_and_fallbacks(monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_FALLBACK_MODELS", raising=False)

    refreshed = importlib.reload(config)

    assert refreshed.GEMINI_MODEL == "gemini-1.5-flash"
    assert refreshed.GEMINI_FALLBACK_MODELS == [
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
    ]
