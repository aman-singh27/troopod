from bs4 import BeautifulSoup
from app.models import Modification
from typing import List

def apply_modifications(raw_html: str, modifications: List[Modification], original_url: str) -> str:
    """Apply modifications to HTML using BeautifulSoup"""
    try:
        soup = BeautifulSoup(raw_html, "lxml")
        
        applied_count = 0
        for mod in modifications:
            try:
                # Find matching element
                if mod.element_type == "h1":
                    element = soup.find("h1", string=lambda x: x and mod.original_text in x)
                elif mod.element_type == "h2":
                    element = soup.find("h2", string=lambda x: x and mod.original_text in x)
                elif mod.element_type == "h3":
                    element = soup.find("h3", string=lambda x: x and mod.original_text in x)
                elif mod.element_type == "cta_button":
                    element = soup.find("button", string=lambda x: x and mod.original_text in x)
                    if not element:
                        element = soup.find("a", class_=lambda x: x and "btn" in x.lower(), 
                                          string=lambda x: x and mod.original_text in x)
                elif mod.element_type == "hero_subtext":
                    element = soup.find("p", string=lambda x: x and mod.original_text in x)
                elif mod.element_type == "meta_description":
                    element = soup.find("meta", {"name": "description"})
                else:
                    element = None
                
                if element:
                    if mod.element_type == "meta_description":
                        element["content"] = mod.replacement_text
                    else:
                        element.string = mod.replacement_text
                    applied_count += 1
            except Exception as e:
                print(f"Warning: Could not apply modification {mod.element_type}: {e}")
                continue
        
        # Inject personalization banner
        body = soup.find("body")
        if body:
            banner_html = """<div id="adaptlp-banner" style="position: fixed; bottom: 20px; right: 20px; background: #7c3aed; color: white; padding: 12px 20px; border-radius: 9999px; font-size: 12px; z-index: 9999; box-shadow: 0 0 40px rgba(124, 58, 237, 0.15); display: flex; align-items: center; gap: 10px;">
                <span>✦ Personalized for this ad by AdaptLP</span>
                <button onclick="document.getElementById('adaptlp-banner').style.display='none'" style="background: none; border: none; color: white; cursor: pointer; font-size: 16px; padding: 0;">×</button>
            </div>"""
            body.append(BeautifulSoup(banner_html, "html.parser"))
        
        # Ensure base href exists
        head = soup.find("head")
        if head and not soup.find("base"):
            base_tag = BeautifulSoup(f'<base href="{original_url}">', "html.parser")
            head.insert(0, base_tag)
        
        return str(soup)
    
    except Exception as e:
        print(f"Error applying modifications: {e}")
        return raw_html
