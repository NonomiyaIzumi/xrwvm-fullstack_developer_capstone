"""
Drives the live Render deployment through the golden path with Playwright
and saves the deployed-app screenshots the submission needs (tasks 25-28).
Mirrors capture_screenshots.py but points at the public deployment URL.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from browsershot import save_with_address_bar

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "submission_assets"
BASE_URL = "https://dealership-web.onrender.com"

DEMO_USER = {
    "userName": "janedoe",
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "janedoe@example.com",
    "password": "DealershipDemo2026!",
}


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # --- 1. Deployed landing page (before login) ------------------------------------
        page.goto(BASE_URL, timeout=90000)
        page.wait_for_selector("table.dealer-table", timeout=30000)
        save_with_address_bar(page, OUT_DIR / "deployed_landingpage.png")
        print("Captured deployed_landingpage.png")

        # --- Register (idempotent-ish) then ensure logged in -----------------------------
        page.goto(f"{BASE_URL}/register")
        page.fill("input[name=userName]", DEMO_USER["userName"])
        page.fill("input[name=firstName]", DEMO_USER["firstName"])
        page.fill("input[name=lastName]", DEMO_USER["lastName"])
        page.fill("input[name=email]", DEMO_USER["email"])
        page.fill("input[name=password]", DEMO_USER["password"])
        page.click("button:has-text('Register')")
        page.wait_for_timeout(1000)

        page.goto(f"{BASE_URL}/login")
        if page.url.rstrip("/").endswith("/login"):
            inputs = page.locator("form.auth-form input")
            inputs.nth(0).fill(DEMO_USER["userName"])
            inputs.nth(1).fill(DEMO_USER["password"])
            page.click("button:has-text('Login')")
            page.wait_for_timeout(1000)

        # --- 2. Deployed logged-in page ---------------------------------------------------
        page.goto(BASE_URL)
        page.wait_for_selector("table.dealer-table")
        page.wait_for_selector("text=Review Dealer")
        save_with_address_bar(page, OUT_DIR / "deployed_loggedin.png")
        print("Captured deployed_loggedin.png")

        # --- 3. Deployed dealer detail page -----------------------------------------------
        page.goto(f"{BASE_URL}/dealer/1")
        page.wait_for_selector("text=Reviews")
        page.wait_for_selector("text=Loading reviews", state="detached", timeout=15000)
        save_with_address_bar(page, OUT_DIR / "deployed_dealer_detail.png", full_page=True)
        print("Captured deployed_dealer_detail.png")

        # --- 4. Post a review, then screenshot it showing on the deployed site -----------
        page.goto(f"{BASE_URL}/postreview/1")
        page.wait_for_selector("form.review-form")
        page.fill("input[name=name]", "Jane Doe")
        page.fill("textarea[name=review]", "Great communication and a smooth, no-pressure buying experience.")
        page.select_option("select[name=car_model]", label="Toyota Camry")
        page.fill("input[name=car_year]", "2022")
        page.click("button:has-text('Post Review')")
        page.wait_for_timeout(2000)

        page.goto(f"{BASE_URL}/dealer/1")
        page.wait_for_selector("text=Jane Doe")
        page.wait_for_timeout(300)
        save_with_address_bar(page, OUT_DIR / "deployed_add_review.png", full_page=True)
        print("Captured deployed_add_review.png")

        browser.close()


if __name__ == "__main__":
    main()
