import httpx
from bs4 import BeautifulSoup
from app.config import REQUEST_TIMEOUT_SECONDS, MAX_HTML_SIZE_KB
from app.models import LPContent

class LPFetchError(Exception):
    pass


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
            
        # Extract hero subtext (first p after h1 or in header)
        hero_subtext = ""
        header = soup.find("header")
        if header:
            p_tag = header.find("p")
            if p_tag:
                hero_subtext = p_tag.get_text(strip=True)
            
        if not hero_subtext:
            if h1_tag:
                next_p = h1_tag.find_next("p")
                if next_p:
                    hero_subtext = next_p.get_text(strip=True)
            else:
                p_tags = soup.find_all("p")
                if p_tags:
                    hero_subtext = p_tags[0].get_text(strip=True)
            
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
