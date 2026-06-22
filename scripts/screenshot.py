"""Screenshot the running Streamlit UI (http://localhost:8520) -> assets/demo.png.

Requires the app running (`python -m streamlit run app.py`) and Playwright with a chromium browser.
"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'demo.png')
URL = os.environ.get('UI_URL', 'http://localhost:8520')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 920, 'height': 680}, device_scale_factor=2)
    page.goto(URL, wait_until='domcontentloaded')
    try:
        page.wait_for_selector('div[role="alert"]', timeout=90000)  # the green answer box
    except Exception:
        page.wait_for_timeout(15000)
    page.wait_for_timeout(700)
    page.screenshot(path=OUT)
    browser.close()
print('wrote', OUT)
