import httpx
from bs4 import BeautifulSoup
from app.config import REQUEST_TIMEOUT_SECONDS, MAX_HTML_SIZE_KB
from app.models import LPContent

class LPFetchError(Exception):
    pass


def _normalize_text(value: str | None) -> str:
    return " ".join((value or "").split()).strip()


def _is_meaningful_paragraph(tag) -> bool:
    if not tag:
        return False

    text = _normalize_text(tag.get_text(" ", strip=True))
    if not text or len(text) < 15:
        return False

    class_name = " ".join(tag.get("class", [])).lower() if tag.get("class") else ""
    if any(token in class_name for token in ("hero", "lead", "subtitle", "subtext", "strap", "intro")):
        return True

    if any(token in text.lower() for token in ("free", "save", "start", "try", "sign up", "book", "learn")):
        return True

    return len(text) >= 30 or any(punctuation in text for punctuation in (".", "!", "?"))


def _extract_hero_subtext(soup: BeautifulSoup, h1_tag) -> str:
    header = soup.find("header")
    if header:
        header_paragraphs = header.find_all("p")
        for paragraph in header_paragraphs:
            if _is_meaningful_paragraph(paragraph):
                return _normalize_text(paragraph.get_text(" ", strip=True))

    if h1_tag:
        for paragraph in h1_tag.find_all_next("p"):
            if _is_meaningful_paragraph(paragraph):
                return _normalize_text(paragraph.get_text(" ", strip=True))

    for paragraph in soup.find_all("p"):
        if _is_meaningful_paragraph(paragraph):
            return _normalize_text(paragraph.get_text(" ", strip=True))

    return ""


async def _fetch_page(url: str, verify: bool) -> httpx.Response:
    async with httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT_SECONDS,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible bot)"},
        verify=verify,
    ) as client:
        return await client.get(url)

async def fetch_and_parse(url: str) -> LPContent:
    """Fetch and parse landing page HTML"""
    try:
        try:
            response = await _fetch_page(url, verify=True)
        except httpx.ConnectError:
            # Retry with relaxed SSL verification for hosts with incomplete cert chain.
            response = await _fetch_page(url, verify=False)
            
        if response.status_code != 200:
            raise LPFetchError(f"Failed to fetch page: HTTP {response.status_code}")
            
        if len(response.content) > MAX_HTML_SIZE_KB * 1024:
            raise LPFetchError(f"Page too large (> {MAX_HTML_SIZE_KB}KB)")
            
        html = response.text
        soup = BeautifulSoup(html, "lxml")
            
        # Extract content
        title = soup.title.string if soup.title else ""
        h1_tag = soup.find("h1")
        h1 = h1_tag.get_text(strip=True) if h1_tag else ""
            
        h2s = [tag.get_text(strip=True) for tag in soup.find_all("h2")[:5]]
        h3s = [tag.get_text(strip=True) for tag in soup.find_all("h3")[:5]]
            
        meta_desc = ""
        meta_tag = soup.find("meta", {"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"]
            
        hero_subtext = _extract_hero_subtext(soup, h1_tag)
            
        # Extract CTA buttons
        cta_buttons = []
        for btn in soup.find_all("button")[:5]:
            btn_text = btn.get_text(strip=True)
            if btn_text:
                cta_buttons.append(btn_text)
        for link in soup.find_all("a", class_=lambda x: x and "btn" in x.lower())[:5]:
            link_text = link.get_text(strip=True)
            if link_text and link_text not in cta_buttons:
                cta_buttons.append(link_text)
            
        # Inject base href
        if "<head>" in html:
            html = html.replace("<head>", f'<head>\n<base href="{url}">')
        elif "<HEAD>" in html:
            html = html.replace("<HEAD>", f'<HEAD>\n<base href="{url}">')
            
        return LPContent(
            title=title,
            h1=h1,
            h2s=h2s,
            h3s=h3s,
            meta_description=meta_desc,
            cta_buttons=cta_buttons,
            hero_subtext=hero_subtext,
            raw_html=html,
        )
    
    except LPFetchError:
        raise
    except Exception as e:
        raise LPFetchError(f"Error fetching landing page: {str(e)}")
