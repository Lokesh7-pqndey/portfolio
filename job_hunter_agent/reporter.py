"""
Daily Application Reporter Module.
Generates structured markdown and terminal reports of jobs applied today.
"""
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config import REPORTS_DIR, CANDIDATE_PROFILE
from database import get_today_applied_jobs, get_overall_stats

# Ensure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def generate_daily_report() -> str:
    """
    Generates and saves the daily job application report in Markdown format.
    """
    today_jobs = get_today_applied_jobs()
    stats = get_overall_stats()
    today_str = datetime.now().strftime("%Y-%m-%d")
    timestamp_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    
    report_lines = [
        f"# 📊 Daily Job Application Intelligence Report",
        f"> **Candidate:** {CANDIDATE_PROFILE['full_name']} | **Date:** {timestamp_str}",
        f"> **Portfolio:** [{CANDIDATE_PROFILE['portfolio_url']}]({CANDIDATE_PROFILE['portfolio_url']}) | **Resume:** [{CANDIDATE_PROFILE['portfolio_url']}/resume.pdf]({CANDIDATE_PROFILE['portfolio_url']}/resume.pdf)",
        f"",
        f"---",
        f"",
        f"### 📈 Executive Application Summary",
        f"- **Jobs Applied Today:** `{len(today_jobs)}`",
        f"- **Total Career Applications (All-Time):** `{stats['total_applied']}`",
        f"- **Average Match Quality:** `{stats['average_match_score']}%`",
        f"",
        f"---",
        f"",
        f"### 📋 Jobs Applied Today ({today_str})"
    ]
    
    if not today_jobs:
        report_lines.append("\n*No new jobs applied today. Run `python main.py run` to scan and apply to active openings.*")
    else:
        report_lines.append("")
        report_lines.append("| # | Company | Job Title | Location | Match | Key Matched Skills | Direct Link |")
        report_lines.append("|---|---------|-----------|----------|:-----:|--------------------|:-----------:|")
        
        for idx, job in enumerate(today_jobs, 1):
            title = job["title"]
            company = job["company"]
            loc = job["location"] or "India / Remote"
            score = f"{job['match_score']:.0f}%"
            skills = job["matched_skills"] or "SQL, Python, Power BI"
            url = job["job_url"]
            link_md = f"[Open Job ↗]({url})" if url else "N/A"
            
            report_lines.append(f"| {idx} | **{company}** | {title} | {loc} | `{score}` | {skills} | {link_md} |")
            
    report_lines.extend([
        f"",
        f"---",
        f"",
        f"### 🎯 Profile & Pitch Highlight Used Today",
        f"- **Target Roles:** Data Analyst, SQL Developer, BI Analyst, Power BI Developer",
        f"- **Core Experience Highlighted:** Reliance Retail (4+ Years, 1,000+ SKUs in SAP, 15% Stock Variance Reduction)",
        f"- **Flagship Technical Proof:**",
        f"  1. *Netflix Content Strategy & Catalog Intelligence* (6,200+ titles, 2,445 cleaned records, 68% movies vs 32% TV)",
        f"  2. *Swiggy Churn Prediction ML* (150K+ orders, 0.91 ROC AUC Random Forest, ₹964M revenue modeled)",
        f"  3. *Mutual Fund Alpha Dashboard* (Power BI Star Schema, DAX Sharpe Ratio, Drawdown vs NIFTY 50)",
        f"",
        f"---",
        f"*Report generated automatically by Lokesh's Job Hunter Agent.*"
    ])
    
    full_report = "\n".join(report_lines)
    
    # Save report to file
    report_file = Path(REPORTS_DIR) / f"daily_report_{today_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(full_report)
        
    return full_report

def print_daily_summary():
    """Prints the daily report cleanly to the console."""
    report = generate_daily_report()
    print("\n" + "="*80)
    print(report)
    print("="*80 + "\n")
