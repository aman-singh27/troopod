from app.services import gemini


def test_model_candidates_unique_and_ordered(monkeypatch):
    monkeypatch.setattr(gemini, "GEMINI_MODEL", "gemini-2.5-flash")
    monkeypatch.setattr(
        gemini,
        "GEMINI_FALLBACK_MODELS",
        ["gemini-flash-latest", "gemini-2.0-flash", "gemini-2.5-flash"],
    )

    candidates = gemini._model_candidates()
    assert candidates == ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash"]
