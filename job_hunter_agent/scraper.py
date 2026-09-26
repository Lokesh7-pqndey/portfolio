"""
Job Scraper & Discovery Module.
Finds active job postings for Data Analyst, SQL Developer, and BI roles
across public job feeds and aggregators.
"""
import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict
from config import JOB_SEARCH_CRITERIA

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_linkedin_public_jobs(keywords: str = "Data Analyst", location: str = "India", limit: int = 15) -> List[Dict]:
    """
    Fetches real active job postings from LinkedIn's public guest job search endpoint.
    No login required for discovery!
    """
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={requests.utils.quote(keywords)}&location={requests.utils.quote(location)}&start=0"
    jobs = []
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=12)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("li")
            
            for card in job_cards:
                title_el = card.find("h3", class_="base-search-card__title")
                company_el = card.find("h4", class_="base-search-card__subtitle")
                location_el = card.find("span", class_="job-search-card__location")
                link_el = card.find("a", class_="base-card__full-link")
                
                if title_el and company_el and link_el:
                    title = title_el.get_text(strip=True)
                    company = company_el.get_text(strip=True)
                    loc = location_el.get_text(strip=True) if location_el else location
                    raw_link = link_el.get("href", "")
                    clean_link = raw_link.split("?")[0]
                    
                    # Extract unique job ID
                    match = re.search(r'(\d+)', clean_link)
                    job_id = f"li_{match.group(1)}" if match else f"li_{hash(clean_link)}"
                    
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": loc,
                        "platform": "LinkedIn",
                        "job_url": clean_link,
                        # Approximate snippet from title/metadata for matching
                        "description": f"{title} at {company} in {loc}. Requires SQL, Python, Power BI, data analysis, reporting."
                    })
                    if len(jobs) >= limit:
                        break
    except Exception as e:
        print(f"[Warning] LinkedIn Guest search error: {e}")
        
    return jobs

def fetch_remote_jobs(limit: int = 10) -> List[Dict]:
    """
    Fetches remote data analytics jobs from public remote API.
    """
    url = "https://remoteok.com/api?tag=data"
    jobs = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for item in data[1:]:  # first item is legal info
                title = item.get("position", "")
                company = item.get("company", "")
                desc = item.get("description", "")
                apply_url = item.get("url", "")
                job_id = f"rok_{item.get('id', hash(apply_url))}"
                
                if any(t.lower() in title.lower() for t in ["data", "analyst", "sql", "bi", "analytics"]):
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": "Remote",
                        "platform": "RemoteOK",
                        "job_url": apply_url,
                        "description": desc[:1000]
                    })
                if len(jobs) >= limit:
                    break
    except Exception as e:
        print(f"[Warning] RemoteOK fetch error: {e}")
    return jobs

def discover_all_jobs() -> List[Dict]:
    """
    Aggregates job postings across multiple search keywords and locations.
    """
    all_jobs = []
    seen_ids = set()
    
    # 1. Search LinkedIn for target titles & locations
    search_queries = [
        ("Data Analyst", "India"),
        ("SQL Developer", "India"),
        ("Power BI Analyst", "India"),
        ("Data Analyst", "Remote")
    ]
    
    for kw, loc in search_queries:
        print(f"[*] Discovering jobs for '{kw}' in '{loc}'...")
        results = fetch_linkedin_public_jobs(keywords=kw, location=loc, limit=8)
        for job in results:
            if job["job_id"] not in seen_ids:
                seen_ids.add(job["job_id"])
                all_jobs.append(job)
                
    # 2. Add Remote jobs
    remote_jobs = fetch_remote_jobs(limit=5)
    for rj in remote_jobs:
        if rj["job_id"] not in seen_ids:
            seen_ids.add(rj["job_id"])
            all_jobs.append(rj)
            
    print(f"[+] Total unique jobs discovered: {len(all_jobs)}")
    return all_jobs
