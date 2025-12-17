"""
Standalone Playwright worker script.
Called via subprocess to avoid asyncio conflicts with uvicorn on Windows.
"""
import sys
import json


def fetch_youtube_page(url: str) -> dict:
    """Fetch YouTube page and extract channel ID."""
    from playwright.sync_api import sync_playwright
    
    CONSENT_SELECTORS = [
        'button:has-text("Accept all")',
        'button:has-text("Accept")',
        'button:has-text("I agree")',
        'button[aria-label="Accept all"]',
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="en-US"
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # Click consent button if present
            for selector in CONSENT_SELECTORS:
                try:
                    button = page.locator(selector).first
                    if button.is_visible(timeout=1000):
                        button.click()
                        page.wait_for_timeout(2000)
                        break
                except:
                    continue
            
            # If still on consent page, navigate again
            if "consent" in page.url.lower():
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)
            
            html = page.content()
            title = page.title()
            
            return {
                "success": True,
                "html": html,
                "title": title,
                "url": page.url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "URL required"}))
        sys.exit(1)
    
    url = sys.argv[1]
    result = fetch_youtube_page(url)
    print(json.dumps(result))
