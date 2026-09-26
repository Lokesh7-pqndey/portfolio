"""
Configuration file for Lokesh's Autonomous Job Hunter & Application Agent.
Stores candidate profile information, job search criteria, and scoring thresholds.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# --- Candidate Profile Information ---
CANDIDATE_PROFILE = {
    "full_name": "Lokesh Pandey",
    "email": "pandeylokesh87@gmail.com",
    "phone": "+91-9456382363",
    "location": "Udham Singh Nagar, Uttarakhand, India",
    "portfolio_url": "https://lokesh-pandey-six.vercel.app",
    "github_url": "https://github.com/Lokesh7-pqndey",
    "linkedin_url": "https://linkedin.com/in/lokesh-pandey-2265b5218",
    "resume_path": str(PROJECT_ROOT / "resume.pdf"),
    
    # Core Experience & Answers for Common Application Form Questions
    "years_of_experience": 4,
    "current_company": "Reliance Retail (Managed Services)",
    "current_title": "Department Manager — Data & Operations",
    "notice_period_days": 15,
    "expected_ctc_lpa": "6.5 - 9.0 LPA",
    "current_ctc_lpa": "Negotiable",
    
    # Standard Form Answers
    "answers": {
        "sql_experience": "4+ years writing complex queries, window functions, CTEs, and query optimization.",
        "python_experience": "2+ years in exploratory data analysis (Pandas, NumPy, Seaborn) and predictive modeling (Scikit-Learn).",
        "powerbi_experience": "3+ years building interactive multi-page dashboards, Star Schemas, and custom DAX measures.",
        "excel_experience": "4+ years in advanced formulas, XLOOKUP, Pivot Tables, and automated executive reporting.",
        "why_hire_me": "Data Analyst with 4+ years of real-world operations experience at Reliance Retail (15% stock variance reduction) paired with technical data science expertise (0.91 ROC AUC ML, complex SQL CTEs, Power BI DAX). I translate raw database records into direct revenue and operational efficiency."
    }
}

# --- Core Skill Matrix for JD Matching ---
SKILL_WEIGHTS = {
    # High Priority (Core Data Analytics)
    "sql": 15,
    "postgresql": 10,
    "mysql": 10,
    "python": 15,
    "pandas": 10,
    "power bi": 15,
    "dax": 10,
    "excel": 10,
    "data analysis": 15,
    "eda": 10,
    
    # Operational & Modeling
    "sap": 8,
    "machine learning": 8,
    "scikit-learn": 8,
    "k-means": 6,
    "rfm": 6,
    "random forest": 6,
    "reporting": 8,
    "dashboard": 10,
    "business intelligence": 10,
    "statistics": 8
}

# --- Job Search Criteria ---
JOB_SEARCH_CRITERIA = {
    "target_titles": [
        "Data Analyst",
        "SQL Developer",
        "Business Intelligence Analyst",
        "Power BI Developer",
        "Junior Data Analyst",
        "Data Analytics Specialist",
        "Product Analyst",
        "Operations Analyst"
    ],
    "target_locations": [
        "Remote",
        "Noida",
        "Gurugram",
        "Delhi NCR",
        "Bengaluru",
        "Mumbai",
        "Pune",
        "Dehradun"
    ],
    "min_match_score": 55,  # Qualified threshold (55%+)
    "auto_apply_limit_per_day": 20,  # Safety cap per day
}

# --- Database & Reports Paths ---
DB_PATH = str(BASE_DIR / "applications.db")
REPORTS_DIR = str(BASE_DIR / "reports")
SESSIONS_DIR = str(BASE_DIR / "browser_sessions")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)
