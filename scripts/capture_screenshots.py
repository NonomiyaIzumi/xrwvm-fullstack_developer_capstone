"""
Drives the real, locally-running capstone app (Django + React + Node/Mongo +
Flask sentiment service, all already started) through the golden path with
Playwright (headless Chromium/Edge) and saves the screenshots the submission
needs. See browsershot.py for why this uses an in-page screenshot + synthetic
address-bar overlay instead of an OS-level window capture.
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from browsershot import save_with_address_bar

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "submission_assets"
BASE_URL = os.environ.get("CAPSTONE_BASE_URL", "http://localhost:8000")

# These are throwaway credentials for a local/ephemeral demo database only.
# Never reuse them for a real deployment - set DJANGO_SUPERUSER_PASSWORD (and
# a fresh demo-user password) to your own values there instead.
DEMO_USER = {
    "userName": "janedoe",
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "janedoe@example.com",
    "password": os.environ.get("CAPSTONE_DEMO_PASSWORD", "DealershipDemo2026!"),
}

ADMIN_USER = os.environ.get("CAPSTONE_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("CAPSTONE_ADMIN_PASSWORD", "Capstone2026Admin!")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # --- 1. Home page before login ------------------------------------------------
        page.goto(f"{BASE_URL}/")
        page.wait_for_selector("table.dealer-table")
        save_with_address_bar(page, OUT_DIR / "get_dealers.png")
        print("Captured get_dealers.png")

        # --- Register the demo user (idempotent-ish: ignore failure if already exists) -
        page.goto(f"{BASE_URL}/register")
        page.fill("input[name=userName]", DEMO_USER["userName"])
        page.fill("input[name=firstName]", DEMO_USER["firstName"])
        page.fill("input[name=lastName]", DEMO_USER["lastName"])
        page.fill("input[name=email]", DEMO_USER["email"])
        page.fill("input[name=password]", DEMO_USER["password"])
        page.click("button:has-text('Register')")
        page.wait_for_timeout(800)

        if "/login" not in page.url and page.locator("text=Already Registered").count() == 0:
            pass  # registered + auto logged-in
        else:
            # Already registered from a previous run -> log in explicitly.
            page.goto(f"{BASE_URL}/login")
            page.fill("input", "")  # no-op safeguard
        # Ensure logged in either way:
        page.goto(f"{BASE_URL}/login")
        if page.url.rstrip("/").endswith("/login"):
            inputs = page.locator("form.auth-form input")
            inputs.nth(0).fill(DEMO_USER["userName"])
            inputs.nth(1).fill(DEMO_USER["password"])
            page.click("button:has-text('Login')")
            page.wait_for_timeout(800)

        # --- 2. Home page after login (Review Dealer + username + URL) -----------------
        page.goto(f"{BASE_URL}/")
        page.wait_for_selector("table.dealer-table")
        page.wait_for_selector("text=Review Dealer")
        save_with_address_bar(page, OUT_DIR / "get_dealers_loggedin.png")
        print("Captured get_dealers_loggedin.png")

        # --- 3. Dealers filtered by state (Kansas) --------------------------------------
        page.goto(f"{BASE_URL}/dealers/Kansas")
        page.wait_for_selector("table.dealer-table")
        page.wait_for_timeout(300)
        save_with_address_bar(page, OUT_DIR / "dealersbystate.png")
        print("Captured dealersbystate.png")

        # --- 4. Dealer detail + reviews --------------------------------------------------
        page.goto(f"{BASE_URL}/dealer/1")
        page.wait_for_selector("text=Reviews")
        page.wait_for_selector("text=Loading reviews", state="detached", timeout=15000)
        save_with_address_bar(page, OUT_DIR / "dealer_id_reviews.png", full_page=True)
        print("Captured dealer_id_reviews.png")

        # --- 5. Post review form (before submit) -----------------------------------------
        page.goto(f"{BASE_URL}/postreview/1")
        page.wait_for_selector("form.review-form")
        page.fill("input[name=name]", "Jane Doe")
        page.fill("textarea[name=review]", "The sales team was fast, friendly, and very transparent about pricing.")
        page.select_option("select[name=car_model]", label="Toyota Camry")
        page.fill("input[name=car_year]", "2022")
        save_with_address_bar(page, OUT_DIR / "dealership_review_submission.png")
        print("Captured dealership_review_submission.png")

        page.click("button:has-text('Post Review')")
        page.wait_for_timeout(1600)

        # --- 6. Added review visible on the dealer page -----------------------------------
        page.goto(f"{BASE_URL}/dealer/1")
        page.wait_for_selector("text=Jane Doe")
        page.wait_for_timeout(300)
        save_with_address_bar(page, OUT_DIR / "added_review.png", full_page=True)
        print("Captured added_review.png")

        # --- 7. Django admin login ---------------------------------------------------------
        page.goto(f"{BASE_URL}/admin/login/")
        page.fill("#id_username", ADMIN_USER)
        page.fill("#id_password", ADMIN_PASSWORD)
        page.click("input[type=submit]")
        page.wait_for_selector("text=Site administration")
        save_with_address_bar(page, OUT_DIR / "admin_login.png")
        print("Captured admin_login.png")

        # --- 8. Django admin logout (admin's logout form is POST-only, so click it) --------
        page.click("#logout-form button")
        page.wait_for_timeout(300)
        save_with_address_bar(page, OUT_DIR / "admin_logout.png")
        print("Captured admin_logout.png")

        browser.close()


if __name__ == "__main__":
    main()
