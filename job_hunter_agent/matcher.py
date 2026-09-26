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
    missing_skills = []
    total_weight = sum(SKILL_WEIGHTS.values())
    earned_weight = 0
    
    for skill, weight in SKILL_WEIGHTS.items():
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            matched_skills.append(skill.title())
            earned_weight += weight
            
    # Calculate score normalized to 100%
    if matched_skills:
        raw_pct = (earned_weight / total_weight) * 100
        # If core skills (SQL + Python + Power BI) are present, boost score
        core_count = sum(1 for s in ["sql", "python", "power bi"] if re.search(r'\b' + s + r'\b', text))
        boost = core_count * 10
        score = min(100.0, round(raw_pct * 1.5 + boost, 1))
    else:
        score = 25.0  # Baseline for matching title
        
    # Check title alignment
    title_match = any(t.lower() in title.lower() for t in JOB_SEARCH_CRITERIA["target_titles"])
    if title_match:
        score = min(100.0, score + 15)

    is_qualified = score >= JOB_SEARCH_CRITERIA["min_match_score"]
    
    # Generate tailored pitch
    tailored_pitch = generate_tailored_pitch(title, matched_skills)

    return {
        "title": title,
        "match_score": score,
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
