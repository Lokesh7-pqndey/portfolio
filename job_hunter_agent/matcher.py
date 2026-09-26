"""
Job Matcher & Application Optimization Engine.
Analyzes job descriptions, calculates relevance scores against Lokesh's skills,
and generates tailored cover notes / screening answers.
"""
import re
from typing import Dict, List, Tuple
from config import CANDIDATE_PROFILE, SKILL_WEIGHTS, JOB_SEARCH_CRITERIA

def analyze_job(title: str, description: str) -> Dict:
    """
    Evaluates a job posting description against candidate skills.
    Returns match percentage, matched skills, missing skills, and tailored pitch.
    """
    text = (title + " " + description).lower()
    
    matched_skills = []
    
    # Realistic skill weights
    skill_values = {
        "sql": 20,
        "postgresql": 10,
        "mysql": 10,
        "python": 15,
        "pandas": 10,
        "power bi": 15,
        "powerbi": 15,
        "dax": 10,
        "excel": 10,
        "tableau": 10,
        "data analysis": 15,
        "analytics": 10,
        "database": 10,
        "reporting": 10,
        "dashboard": 10,
        "sap": 8,
        "machine learning": 10,
        "statistics": 8
    }
    
    score = 0.0
    
    # Check title alignment (baseline 35%)
    target_terms = ["data analyst", "sql developer", "business intelligence", "power bi", "analytics", "analyst", "database"]
    if any(t in title.lower() for t in target_terms):
        score += 35.0
        
    for skill, val in skill_values.items():
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            display_name = "Power BI" if skill == "powerbi" else skill.title()
            if display_name not in matched_skills:
                matched_skills.append(display_name)
                score += val
                
    # Normalize score
    final_score = min(98.0, round(score, 1)) if score > 0 else 25.0
    is_qualified = final_score >= 50.0
    
    # Generate tailored pitch
    tailored_pitch = generate_tailored_pitch(title, matched_skills)

    return {
        "title": title,
        "match_score": final_score,
        "is_qualified": is_qualified,
        "matched_skills": matched_skills,
        "matched_skills_str": ", ".join(matched_skills[:8]),
        "tailored_pitch": tailored_pitch
    }

def generate_tailored_pitch(job_title: str, matched_skills: List[str]) -> str:
    """
    Generates an executive, concise cover pitch tailored to the specific role.
    """
    skills_str = ", ".join(matched_skills[:4]) if matched_skills else "SQL, Python, and Power BI"
    
    pitch = (
        f"Hi Hiring Team,\n\n"
        f"I am writing to express my strong interest in the {job_title} position. "
        f"With 4+ years of business operations experience at Reliance Retail (where I led inventory analytics "
        f"across 1,000+ SKUs in SAP and reduced stock variance by 15%), I specialize in owning the complete data lifecycle: "
        f"relational SQL pipelines, Python data cleansing, and executive Power BI dashboards.\n\n"
        f"Key accomplishments directly aligned with your stack ({skills_str}):\n"
        f"• End-to-End Analytics: Modeled 150K+ consumer records, trained a 0.91 ROC AUC Random Forest classifier, and deployed live scoring via Flask.\n"
        f"• Catalog Intelligence: Cleaned 6,200+ records and resolved 2,400+ missing values in Netflix streaming analytics.\n"
        f"• Institutional BI: Built Star Schema Power BI models benchmarking funds against market indices using dynamic DAX.\n\n"
        f"I would welcome the opportunity to discuss how my analytical rigor and operational background can drive measurable impact for your team.\n\n"
        f"Live Portfolio: {CANDIDATE_PROFILE['portfolio_url']}\n"
        f"GitHub: {CANDIDATE_PROFILE['github_url']}\n"
        f"Best regards,\n"
        f"{CANDIDATE_PROFILE['full_name']} | {CANDIDATE_PROFILE['phone']} | {CANDIDATE_PROFILE['email']}"
    )
    return pitch

def get_answer_for_question(question_text: str) -> str:
    """
    Predicts and provides the best answer for standard screening questions.
    """
    q = question_text.lower()
    
    if "sql" in q and ("year" in q or "experience" in q):
        return "4"
    elif "python" in q and ("year" in q or "experience" in q):
        return "3"
    elif "power bi" in q or "powerbi" in q:
        return "3"
    elif "excel" in q:
        return "4"
    elif "total" in q and ("experience" in q or "year" in q):
        return str(CANDIDATE_PROFILE["years_of_experience"])
    elif "notice" in q:
        return str(CANDIDATE_PROFILE["notice_period_days"])
    elif "salary" in q or "ctc" in q or "compensation" in q:
        return CANDIDATE_PROFILE["expected_ctc_lpa"]
    elif "portfolio" in q or "website" in q:
        return CANDIDATE_PROFILE["portfolio_url"]
    elif "github" in q:
        return CANDIDATE_PROFILE["github_url"]
    elif "linkedin" in q:
        return CANDIDATE_PROFILE["linkedin_url"]
    elif "phone" in q or "mobile" in q:
        return CANDIDATE_PROFILE["phone"]
    elif "email" in q:
        return CANDIDATE_PROFILE["email"]
    elif "relocate" in q or "willing to relocate" in q:
        return "Yes"
    elif "remote" in q or "hybrid" in q:
        return "Yes"
    elif "sponsor" in q or "visa" in q:
        return "No"
    else:
        return CANDIDATE_PROFILE["answers"]["why_hire_me"]
