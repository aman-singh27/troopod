from app.services import gemini


def test_resolve_api_key_prefers_request_key(monkeypatch):
    monkeypatch.setattr(gemini, "GEMINI_API_KEY", "server-key")
    assert gemini._resolve_api_key("user-key") == "user-key"


def test_resolve_api_key_falls_back_to_server_key(monkeypatch):
    monkeypatch.setattr(gemini, "GEMINI_API_KEY", "server-key")
    assert gemini._resolve_api_key(None) == "server-key"
