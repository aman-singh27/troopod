from fastapi import HTTPException

from app.routes.personalize import _map_gemini_error


def test_quota_error_maps_to_429():
    exc = _map_gemini_error(
        "AI analysis",
        "429 You exceeded your current quota for generate_content",
    )
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 429
    assert "quota" in exc.detail.lower()
    assert "own gemini api key" in exc.detail.lower()


def test_auth_error_maps_to_401():
    exc = _map_gemini_error(
        "AI analysis",
        "No API_KEY or authentication credentials found",
    )
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 401
    assert "api_key" in exc.detail.lower()


def test_generic_error_maps_to_500():
    exc = _map_gemini_error(
        "CRO strategy",
        "unexpected provider failure",
    )
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 500
    assert "CRO strategy failed" in exc.detail
