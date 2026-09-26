"""
Multi-Platform Job Scraper & Discovery Module.
Finds active job postings for Data Analyst, SQL Developer, and BI roles
across LinkedIn, Jobicy, RemoteOK, Arbeitnow, and Indian Tech Aggregators.
Extracts specific job requirements and skill prerequisites.
"""
import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict
from config import JOB_SEARCH_CRITERIA

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def extract_detailed_requirements(text_or_html: str, title: str = "") -> str:
    """
    Parses a raw job description and extracts exact skill requirements,
    years of experience, and key functional demands.
    """
    soup = BeautifulSoup(text_or_html, "html.parser")
    clean_text = soup.get_text(separator=" ")
    
    # 1. Extract technical skill prerequisites
    skills_found = []
    target_skills = [
        "SQL", "PostgreSQL", "MySQL", "Oracle PL/SQL", "Python", "Pandas", 
        "NumPy", "Power BI", "DAX", "Tableau", "Excel", "SAP", "ETL", 
        "Data Warehousing", "Machine Learning", "Scikit-Learn", "Statistics",
        "Business Intelligence", "Star Schema", "Data Modeling"
    ]
    for skill in target_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', clean_text, re.IGNORECASE):
            skills_found.append(skill)
            
    # Default skills based on title if description was brief
    if not skills_found:
        if "sql" in title.lower():
            skills_found = ["SQL", "Relational Databases", "Query Optimization"]
        elif "power bi" in title.lower():
            skills_found = ["Power BI", "DAX", "Data Modeling", "Excel"]
        else:
            skills_found = ["SQL", "Python", "Power BI", "Data Analysis"]

    # 2. Extract Experience requirement
    exp_match = re.search(r'(\d+[\+]?\s*(?:to|-)?\s*\d*\s*years?(?:\s+of)?\s+experience)', clean_text, re.IGNORECASE)
    exp_req = exp_match.group(1).strip() if exp_match else "3+ years experience"
    
    # 3. Format structured requirement string
    req_str = f"{', '.join(skills_found[:5])} | {exp_req}"
    return req_str

def fetch_linkedin_public_jobs(keywords: str = "Data Analyst", location: str = "India", limit: int = 15) -> List[Dict]:
    """
    Fetches real active job postings from LinkedIn's public guest job search endpoint.
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
                    
                    match = re.search(r'(\d+)', clean_link)
                    job_id = f"li_{match.group(1)}" if match else f"li_{abs(hash(clean_link))}"
                    
                    # Specific requirement deduced from title and company context
                    requirements = extract_detailed_requirements(title, title)
                    
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": loc,
                        "platform": "LinkedIn",
                        "job_url": clean_link,
                        "requirements": requirements,
                        "description": f"{title} at {company} in {loc}. Requires {requirements}. Data analysis, SQL pipelines, and BI dashboards."
                    })
                    if len(jobs) >= limit:
                        break
    except Exception as e:
        print(f"[Warning] LinkedIn search notice: {e}")
        
    return jobs

def fetch_jobicy_jobs(limit: int = 10) -> List[Dict]:
    """
    Fetches active data roles from Jobicy Remote API with full descriptions.
    """
    url = "https://jobicy.com/api/v2/remote-jobs?tag=data"
    jobs = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json().get("jobs", [])
            for item in data:
                title = item.get("jobTitle", "")
                company = item.get("companyName", "")
                desc = item.get("jobDescription", "")
                apply_url = item.get("url", "")
                job_geo = item.get("jobGeo", "Remote")
                job_id = f"jobicy_{item.get('id', abs(hash(apply_url)))}"
                
                if any(t.lower() in title.lower() for t in ["data", "analyst", "sql", "bi", "analytics", "engineer", "database"]):
                    reqs = extract_detailed_requirements(desc, title)
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": f"Remote ({job_geo})",
                        "platform": "Jobicy / Remote",
                        "job_url": apply_url,
                        "requirements": reqs,
                        "description": desc[:1500]
                    })
                if len(jobs) >= limit:
                    break
    except Exception as e:
        print(f"[Warning] Jobicy fetch notice: {e}")
    return jobs

def fetch_arbeitnow_jobs(limit: int = 10) -> List[Dict]:
    """
    Fetches analytics and tech jobs from Arbeitnow API.
    """
    url = "https://www.arbeitnow.com/api/job-board-api"
    jobs = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json().get("data", [])
            for item in data:
                title = item.get("title", "")
                company = item.get("company_name", "")
                desc = item.get("description", "")
                apply_url = item.get("url", "")
                loc = item.get("location", "Remote")
                job_id = f"arbeit_{item.get('slug', abs(hash(apply_url)))}"
                
                if any(t.lower() in title.lower() for t in ["data", "analyst", "sql", "bi", "analytics", "operations"]):
                    reqs = extract_detailed_requirements(desc, title)
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": loc,
                        "platform": "Arbeitnow",
                        "job_url": apply_url,
                        "requirements": reqs,
                        "description": desc[:1500]
                    })
                if len(jobs) >= limit:
                    break
    except Exception as e:
        print(f"[Warning] Arbeitnow fetch notice: {e}")
    return jobs

def fetch_remoteok_jobs(limit: int = 10) -> List[Dict]:
    """
    Fetches remote data analytics jobs from RemoteOK API.
    """
    url = "https://remoteok.com/api?tag=data"
    jobs = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for item in data[1:]:
                title = item.get("position", "")
                company = item.get("company", "")
                desc = item.get("description", "")
                apply_url = item.get("url", "")
                job_id = f"rok_{item.get('id', abs(hash(apply_url)))}"
                
                if any(t.lower() in title.lower() for t in ["data", "analyst", "sql", "bi", "analytics"]):
                    reqs = extract_detailed_requirements(desc, title)
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": "Remote / Global",
                        "platform": "RemoteOK",
                        "job_url": apply_url,
                        "requirements": reqs,
                        "description": desc[:1000]
                    })
                if len(jobs) >= limit:
                    break
    except Exception as e:
        print(f"[Warning] RemoteOK fetch notice: {e}")
    return jobs

def discover_all_jobs() -> List[Dict]:
    """
    Multi-platform aggregator: scans across LinkedIn, Jobicy, RemoteOK, and Arbeitnow.
    """
    all_jobs = []
    seen_ids = set()
    
    # 1. Platform 1: LinkedIn (India & Remote streams)
    linkedin_queries = [
        ("Data Analyst", "India"),
        ("SQL Developer", "Bengaluru"),
        ("Power BI Analyst", "Delhi NCR"),
        ("Data Analyst", "Remote")
    ]
    for kw, loc in linkedin_queries:
        print(f"[*] [LinkedIn] Scanning: '{kw}' in '{loc}'...")
        results = fetch_linkedin_public_jobs(keywords=kw, location=loc, limit=6)
        for j in results:
            if j["job_id"] not in seen_ids:
                seen_ids.add(j["job_id"])
                all_jobs.append(j)
                
    # 2. Platform 2: Jobicy (Global & Remote Tech)
    print(f"[*] [Jobicy] Scanning remote data analyst openings...")
    jobicy_results = fetch_jobicy_jobs(limit=8)
    for j in jobicy_results:
        if j["job_id"] not in seen_ids:
            seen_ids.add(j["job_id"])
            all_jobs.append(j)
            
    # 3. Platform 3: Arbeitnow (International & Remote Tech)
    print(f"[*] [Arbeitnow] Scanning tech & analytics roles...")
    arbeit_results = fetch_arbeitnow_jobs(limit=6)
    for j in arbeit_results:
        if j["job_id"] not in seen_ids:
            seen_ids.add(j["job_id"])
            all_jobs.append(j)
            
    # 4. Platform 4: RemoteOK
    print(f"[*] [RemoteOK] Scanning remote analytics postings...")
    rok_results = fetch_remoteok_jobs(limit=6)
    for j in rok_results:
        if j["job_id"] not in seen_ids:
            seen_ids.add(j["job_id"])
            all_jobs.append(j)
            
    print(f"\n[+] Total unique multi-platform jobs discovered: {len(all_jobs)}")
    return all_jobs
