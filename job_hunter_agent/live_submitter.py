"""
Live Application Submitter Module.
Uses automated browser interactions (Playwright) and ATS APIs to fill out
real job application forms, attach candidate resume, and trigger actual
application submissions so that companies send confirmation emails to Lokesh's Gmail.
"""
import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, Optional
from config import CANDIDATE_PROFILE, BASE_DIR

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROOFS_DIR = Path(BASE_DIR) / "submission_proofs"
PROOFS_DIR.mkdir(parents=True, exist_ok=True)

USER_DATA_DIR = Path(BASE_DIR) / "browser_sessions" / "user_data"
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

RESUME_PDF = Path(CANDIDATE_PROFILE["resume_path"])
if not RESUME_PDF.exists():
    RESUME_PDF = Path(BASE_DIR).parent / "resume.pdf"

def launch_persistent_login_window():
    """
    Opens a visible browser for the user to log in once to LinkedIn, Naukri, Hirist, etc.
    All cookies and sessions will be saved in browser_sessions/user_data.
    """
    from playwright.sync_api import sync_playwright
    print("\n" + "="*70)
    print("🔑 ONE-TIME PORTAL LOGIN SESSION")
    print("A browser window is opening.")
    print("Log in to your accounts (LinkedIn, Naukri, Hirist, etc.).")
    print("Your session and cookies will be saved permanently for automated apply!")
    print("Close the browser when you are finished logging in.")
    print("="*70 + "\n")
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR.resolve()),
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.linkedin.com/login")
        print("[*] Browser open. Log into LinkedIn and open tabs for Naukri/Hirist as desired.")
        print("[*] Waiting for browser window to be closed...")
        try:
            # Wait until user closes the window or 5 minutes
            while len(context.pages) > 0 and not page.is_closed():
                time.sleep(1)
        except Exception:
            pass
        context.close()
    print("\n[✓] Session saved! Future applications will run with your authenticated credentials.")

def attempt_live_submission(job: Dict) -> Dict:
    """
    Attempts to submit an actual live application to the company's application portal.
    Captures screenshot proofs and returns submission status.
    """
    job_id = job.get("job_id", "job")
    job_url = job.get("job_url", "")
    title = job.get("title", "")
    company = job.get("company", "")
    platform = job.get("platform", "")
    
    print(f"\n[🌐 LIVE SUBMITTER] Processing: {title} @ {company} ({platform})...")
    print(f"    Target Portal URL: {job_url}")
    
    # Import playwright lazily
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "status": "PLAYWRIGHT_MISSING",
            "message": "Playwright is not installed."
        }
        
    try:
        with sync_playwright() as p:
            # Launch persistent browser context to retain logged-in credentials
            has_session = any(USER_DATA_DIR.iterdir()) if USER_DATA_DIR.exists() else False
            if has_session:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(USER_DATA_DIR.resolve()),
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"],
                    viewport={"width": 1280, "height": 800}
                )
                page = context.pages[0] if context.pages else context.new_page()
                browser = None
            else:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
                )
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
            page.set_default_timeout(25000)
            
            print(f"    Navigating to job portal...")
            try:
                page.goto(job_url, wait_until="domcontentloaded", timeout=25000)
            except Exception as nav_err:
                print(f"    Notice during navigation: {nav_err}")
                
            page.wait_for_timeout(2500)
            
            # Check if there is an "Apply", "Easy Apply", or "Apply Now" button to click
            apply_triggers = [
                'a:has-text("Apply Now")',
                'button:has-text("Apply Now")',
                'a:has-text("Apply for this job")',
                'button:has-text("Apply for this job")',
                'a:has-text("Apply")',
                'button:has-text("Apply")',
                '#apply_button',
                '.apply-button'
            ]
            for selector in apply_triggers:
                try:
                    if page.locator(selector).first.is_visible(timeout=1000):
                        print(f"    Clicking initial apply button ({selector})...")
                        page.locator(selector).first.click()
                        page.wait_for_timeout(2000)
                        break
                except Exception:
                    pass
                    
            # 1. First Name
            first_name_selectors = [
                'input[name*="first_name" i]',
                'input[id*="first_name" i]',
                'input[placeholder*="first name" i]',
                'input[aria-label*="first name" i]'
            ]
            for sel in first_name_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill("Lokesh")
                        print("    [✓] Filled First Name: Lokesh")
                        break
                except Exception:
                    pass
                    
            # 2. Last Name
            last_name_selectors = [
                'input[name*="last_name" i]',
                'input[id*="last_name" i]',
                'input[placeholder*="last name" i]',
                'input[aria-label*="last name" i]'
            ]
            for sel in last_name_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill("Pandey")
                        print("    [✓] Filled Last Name: Pandey")
                        break
                except Exception:
                    pass
                    
            # 3. Full Name (if no first/last split)
            full_name_selectors = [
                'input[name="name"]',
                'input[id="name"]',
                'input[placeholder*="full name" i]',
                'input[name*="applicant_name" i]'
            ]
            for sel in full_name_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill(CANDIDATE_PROFILE["full_name"])
                        print(f"    [✓] Filled Full Name: {CANDIDATE_PROFILE['full_name']}")
                        break
                except Exception:
                    pass
                    
            # 4. Email
            email_selectors = [
                'input[type="email"]',
                'input[name*="email" i]',
                'input[id*="email" i]',
                'input[placeholder*="email" i]'
            ]
            for sel in email_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill(CANDIDATE_PROFILE["email"])
                        print(f"    [✓] Filled Email: {CANDIDATE_PROFILE['email']}")
                        break
                except Exception:
                    pass
                    
            # 5. Phone Number
            phone_selectors = [
                'input[type="tel"]',
                'input[name*="phone" i]',
                'input[id*="phone" i]',
                'input[placeholder*="phone" i]'
            ]
            for sel in phone_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill(CANDIDATE_PROFILE["phone"])
                        print(f"    [✓] Filled Phone: {CANDIDATE_PROFILE['phone']}")
                        break
                except Exception:
                    pass
                    
            # 6. LinkedIn URL
            linkedin_selectors = [
                'input[name*="linkedin" i]',
                'input[id*="linkedin" i]',
                'input[placeholder*="linkedin" i]'
            ]
            for sel in linkedin_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill(CANDIDATE_PROFILE["linkedin_url"])
                        print(f"    [✓] Filled LinkedIn: {CANDIDATE_PROFILE['linkedin_url']}")
                        break
                except Exception:
                    pass
                    
            # 7. Portfolio / Website URL
            portfolio_selectors = [
                'input[name*="website" i]',
                'input[name*="portfolio" i]',
                'input[placeholder*="portfolio" i]',
                'input[placeholder*="website" i]'
            ]
            for sel in portfolio_selectors:
                try:
                    if page.locator(sel).first.is_visible(timeout=500):
                        page.locator(sel).first.fill(CANDIDATE_PROFILE["portfolio_url"])
                        print(f"    [✓] Filled Portfolio: {CANDIDATE_PROFILE['portfolio_url']}")
                        break
                except Exception:
                    pass
                    
            # 8. Resume Upload
            if RESUME_PDF.exists():
                file_inputs = page.locator('input[type="file"]')
                if file_inputs.count() > 0:
                    try:
                        file_inputs.first.set_input_files(str(RESUME_PDF.resolve()))
                        print(f"    [✓] Uploaded Resume File: {RESUME_PDF.name}")
                    except Exception as upload_err:
                        print(f"    Notice during resume file upload: {upload_err}")

            # Capture pre-submit screenshot proof
            clean_company = "".join(c for c in company if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
            proof_before = PROOFS_DIR / f"proof_{clean_company}_{job_id}_form.png"
            page.screenshot(path=str(proof_before), full_page=False)
            print(f"    📸 Application Form Proof: {proof_before.name}")
            
            # 9. Find and Click Final Submit Button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Submit Application")',
                'button:has-text("Submit")',
                'button:has-text("Send Application")'
            ]
            submitted = False
            for sub_sel in submit_selectors:
                try:
                    btn = page.locator(sub_sel).first
                    if btn.is_visible(timeout=1000):
                        print(f"    [🚀] Executing final submission click ({sub_sel})...")
                        btn.click()
                        page.wait_for_timeout(4000)
                        submitted = True
                        break
                except Exception:
                    pass
                    
            # Capture post-submit screenshot proof
            proof_after = PROOFS_DIR / f"proof_{clean_company}_{job_id}_submitted.png"
            page.screenshot(path=str(proof_after), full_page=False)
            
            if browser:
                browser.close()
            else:
                context.close()
            
            return {
                "status": "LIVE_SUBMITTED" if submitted else "FORM_PREPARED",
                "proof_screenshot": str(proof_after if submitted else proof_before),
                "message": "Form successfully filled and submission dispatched." if submitted else "Application form detected & filled; manual captcha check may be required by portal."
            }
            
    except Exception as e:
        print(f"    [!] Notice in live submitter: {e}")
        return {
            "status": "PORTAL_REQUIRES_LOGIN",
            "message": str(e)
        }
