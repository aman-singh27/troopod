from __future__ import annotations

import json
import re
from typing import List, Sequence

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from app.models import Modification


def _normalize_text(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _matches_original(candidate: str, original: str) -> bool:
    candidate_text = _normalize_text(candidate).lower()
    original_text = _normalize_text(original).lower()
    if not candidate_text or not original_text:
        return False
    return candidate_text == original_text or original_text in candidate_text or candidate_text in original_text


def _replace_tag_contents(tag: Tag, replacement_text: str) -> None:
    tag.clear()
    tag.append(NavigableString(replacement_text))


def _find_text_tag(soup: BeautifulSoup, names: Sequence[str], original_text: str) -> Tag | None:
    for name in names:
        for tag in soup.find_all(name):
            if _matches_original(tag.get_text(" ", strip=True), original_text):
                return tag
    return None


def _find_cta_tag(soup: BeautifulSoup, original_text: str) -> Tag | None:
    button_candidates = [
        *soup.find_all("button"),
        *soup.find_all("a"),
        *soup.find_all(attrs={"role": "button"}),
    ]

    for tag in button_candidates:
        class_list = " ".join(tag.get("class", [])).lower() if tag.get("class") else ""
        if class_list and not any(token in class_list for token in ("btn", "cta", "button", "primary", "action")):
            continue
        if _matches_original(tag.get_text(" ", strip=True), original_text):
            return tag
    return None


def _build_fallback_script(modifications: List[Modification]) -> str:
    payload = [
        {
            "element_type": mod.element_type,
            "original_text": mod.original_text,
            "replacement_text": mod.replacement_text,
        }
        for mod in modifications
    ]
    return f"""
<script id="adaptlp-patches">
(function() {{
  const modifications = {json.dumps(payload)};
  const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim().toLowerCase();

  const selectors = {{
    h1: ['h1'],
    h2: ['h2'],
    h3: ['h3'],
    hero_subtext: ['p'],
    cta_button: ['button', 'a', '[role="button"]'],
  }};

  for (const mod of modifications) {{
    if (mod.element_type === 'meta_description') {{
      const meta = document.querySelector('meta[name="description"]');
      if (meta) meta.setAttribute('content', mod.replacement_text);
      continue;
    }}

    const expectedText = normalize(mod.original_text);
    const candidateSelectors = selectors[mod.element_type] || [];

    for (const selector of candidateSelectors) {{
      const elements = document.querySelectorAll(selector);
      for (const element of elements) {{
        const actualText = normalize(element.textContent || element.innerText);
        if (!expectedText || !actualText.includes(expectedText)) continue;
        element.textContent = mod.replacement_text;
        break;
      }}
    }}
  }}
}})();
</script>
""".strip()


def _apply_single_modification(soup: BeautifulSoup, mod: Modification) -> tuple[bool, bool]:
    element: Tag | None = None
    needs_js_fallback = False

    if mod.element_type == "h1":
        element = _find_text_tag(soup, ["h1"], mod.original_text)
        needs_js_fallback = element is None
    elif mod.element_type == "h2":
        element = _find_text_tag(soup, ["h2"], mod.original_text)
        needs_js_fallback = element is None
    elif mod.element_type == "h3":
        element = _find_text_tag(soup, ["h3"], mod.original_text)
        needs_js_fallback = element is None
    elif mod.element_type == "cta_button":
        element = _find_cta_tag(soup, mod.original_text)
        needs_js_fallback = element is None
    elif mod.element_type == "hero_subtext":
        element = _find_text_tag(soup, ["p"], mod.original_text)
        needs_js_fallback = element is None
    elif mod.element_type == "meta_description":
        element = soup.find("meta", {"name": "description"})
        needs_js_fallback = element is None

    if not element:
        return False, needs_js_fallback

    if mod.element_type == "meta_description":
        element["content"] = mod.replacement_text
    else:
        _replace_tag_contents(element, mod.replacement_text)

    return True, False


def apply_modifications(raw_html: str, modifications: List[Modification], original_url: str) -> str:
    """Apply modifications to HTML using BeautifulSoup, then add a JS fallback for misses."""
    try:
        soup = BeautifulSoup(raw_html, "lxml")
        fallback_modifications: list[Modification] = []

        for mod in modifications:
            try:
                applied, needs_js_fallback = _apply_single_modification(soup, mod)
                if needs_js_fallback or not applied:
                    fallback_modifications.append(mod)
            except Exception as exc:
                print(f"Warning: Could not apply modification {mod.element_type}: {exc}")
                fallback_modifications.append(mod)
                continue

        body = soup.find("body")
        if body:
            banner_html = """<div id="adaptlp-banner" style="position: fixed; bottom: 20px; right: 20px; background: #7c3aed; color: white; padding: 12px 20px; border-radius: 9999px; font-size: 12px; z-index: 9999; box-shadow: 0 0 40px rgba(124, 58, 237, 0.15); display: flex; align-items: center; gap: 10px;">
                <span>✦ Personalized for this ad by AdaptLP</span>
                <button onclick="document.getElementById('adaptlp-banner').style.display='none'" style="background: none; border: none; color: white; cursor: pointer; font-size: 16px; padding: 0;">×</button>
            </div>"""
            body.append(BeautifulSoup(banner_html, "html.parser"))

        head = soup.find("head")
        if head and not soup.find("base"):
            base_tag = BeautifulSoup(f'<base href="{original_url}">', "html.parser")
            head.insert(0, base_tag)

        if fallback_modifications and body:
            body.append(BeautifulSoup(_build_fallback_script(fallback_modifications), "html.parser"))

        return str(soup)

    except Exception as exc:
        print(f"Error applying modifications: {exc}")
        return raw_html
