import httpx
from app.config import SCREENSHOTONE_API_KEY, REQUEST_TIMEOUT_SECONDS

class ScreenshotError(Exception):
    pass


async def _try_direct_image_fetch(url: str) -> bytes | None:
    """Return raw bytes when the source URL is already an image."""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
            response = await client.get(url)
            content_type = response.headers.get("content-type", "").lower()
            if response.status_code == 200 and response.content and content_type.startswith("image/"):
                return response.content
    except Exception:
        return None

    return None


async def get_screenshot(url: str) -> bytes:
    """Get screenshot of URL using Screenshotone (primary) or Microlink (fallback)"""
    # If the provided URL is already an image, use it directly.
    direct_image = await _try_direct_image_fetch(url)
    if direct_image:
        return direct_image

    # Try Screenshotone first
    if SCREENSHOTONE_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                response = await client.get(
                    "https://api.screenshotone.com/take",
                    params={
                        "access_key": SCREENSHOTONE_API_KEY,
                        "url": url,
                        "format": "png",
                        "viewport_width": "1280",
                        "viewport_height": "800",
                        "full_page": "false",
                        "delay": "2"
                    }
                )
                
                if response.status_code == 200 and response.content:
                    return response.content
        except Exception as e:
            print(f"Screenshotone failed: {e}")
    
    # Fallback to Microlink
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.get(
                "https://api.microlink.io",
                params={
                    "url": url,
                    "screenshot": "true",
                    "meta": "false",
                    "embed": "screenshot.url"
                }
            )

            if response.status_code == 200:
                content_type = response.headers.get("content-type", "").lower()

                # Some providers return the image bytes directly.
                if content_type.startswith("image/") and response.content:
                    return response.content

                try:
                    data = response.json()
                except ValueError:
                    data = None

                if data:
                    screenshot_url = data.get("data", {}).get("screenshot", {}).get("url")
                    if screenshot_url:
                        # Fetch the actual screenshot image
                        img_response = await client.get(screenshot_url)
                        if img_response.status_code == 200 and img_response.content:
                            return img_response.content
    except Exception as e:
        print(f"Microlink failed: {e}")
    
    raise ScreenshotError("Could not capture screenshot. Both Screenshotone and Microlink failed.")
