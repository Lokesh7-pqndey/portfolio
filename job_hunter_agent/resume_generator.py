"""
Dynamic Overleaf-Style Tailored Resume & Cover Letter Generator.
Creates customized, ATS-optimized resumes and matching cover letters
tailored to each specific job description and company.
"""
import os
from pathlib import Path
from typing import Dict, List
from config import CANDIDATE_PROFILE, BASE_DIR

RESUMES_DIR = Path(BASE_DIR) / "tailored_resumes"
LETTERS_DIR = Path(BASE_DIR) / "cover_letters"

RESUMES_DIR.mkdir(parents=True, exist_ok=True)
LETTERS_DIR.mkdir(parents=True, exist_ok=True)

# Master project bank for contextual ordering
PROJECT_BANK = {
    "netflix": {
        "title": "Netflix Content Strategy & Catalog Intelligence",
        "tech": "Python, Pandas, NumPy, Matplotlib, Seaborn",
        "bullets": [
            "Investigated global streaming content strategy across Netflix's 6,200+ title catalog (2008–2021) to quantify programming mix and geographic sourcing priorities.",
            "Cleaned inconsistent metadata (1,969 missing directors, 476 missing countries) and standardized temporal date structures to enable reliable trend analysis.",
            "Quantified catalog composition: movies account for 68% of titles vs 32% TV shows, with TV-MA established as the dominant rating (33%).",
            "Identified the U.S., India, and U.K. as top producing markets, uncovering repeat director-cast partnerships and guiding audience-targeted catalog balance."
        ],
        "keywords": ["python", "eda", "pandas", "content", "streaming", "media", "seaborn", "matplotlib"]
    },
    "swiggy": {
        "title": "Swiggy End-to-End Data Analytics & Churn Prediction",
        "tech": "SQL, Python, Scikit-Learn, Power BI, Flask API, Docker",
        "bullets": [
            "Tackled an 87.76% customer churn challenge for a Swiggy-style platform by modeling relational data across 150K+ orders and 100K users.",
            "Engineered a 5-table relational SQL pipeline uncovering revenue concentration: 11,419 restaurants drive 80% of INR 964M total revenue.",
            "Built a Random Forest churn classifier (ROC AUC 0.91) using RFM segmentation, identifying purchase recency as the top churn predictor.",
            "Deployed the model as a live Flask scoring API for automated retention offers and built a 5-page Power BI dashboard for executive city-level KPIs."
        ],
        "keywords": ["machine learning", "churn", "scikit-learn", "random forest", "flask", "e-commerce", "rfm", "prediction"]
    },
    "fintech_sql": {
        "title": "Fintech Employee & Salary Analytics SQL Pipeline",
        "tech": "PostgreSQL, Advanced SQL, Window Functions, CTEs",
        "bullets": [
            "Architected production SQL scripts analyzing compensation distributions across 5,000+ employee records using NTILE(4) quartiles and LAG/LEAD functions.",
            "Discovered an 18% structural compensation inversion between newly hired senior engineers and established tenured staff, driving flight risk reduction.",
            "Implemented cumulative payroll window CTEs and departmental percentiles, giving leadership data-backed visibility into department budget disparities."
        ],
        "keywords": ["sql", "postgresql", "mysql", "database", "cte", "window functions", "queries", "pl/sql", "oracle"]
    },
    "mutual_fund": {
        "title": "Mutual Fund Performance Analysis & Alpha Dashboard",
        "tech": "Power BI, DAX Modeling, Star Schema, Python",
        "bullets": [
            "Engineered an institutional wealthtech evaluation suite benchmarking 50+ mutual fund schemes against the NIFTY 50 benchmark.",
            "Modeled a dimensional Star Schema in Power BI with 15+ custom DAX measures (Sharpe Ratio, Alpha vs Benchmark, Maximum Drawdown, CAGR).",
            "Integrated Python automated historical NAV cleansing and sector allocation models to evaluate risk-adjusted return profiles."
        ],
        "keywords": ["power bi", "dax", "dashboard", "star schema", "finance", "wealth", "banking", "reporting", "investment"]
    }
}

def generate_tailored_resume(job: Dict) -> Dict[str, str]:
    """
    Generates an Overleaf/LaTeX styled HTML & Markdown resume customized for this job.
    """
    job_id = job.get("job_id", "job")
    job_title = job.get("title", "Data Analyst")
    company = job.get("company", "Company")
    desc = (job.get("description", "") + " " + job.get("requirements", "")).lower()

    # 1. Tailor Professional Summary
    summary = (
        f"Data Analyst with 4+ years of business operations experience at Reliance Retail and hands-on expertise "
        f"in SQL, Python, and Power BI. Proven track record translating complex datasets into actionable strategic decisions "
        f"— from reducing inventory variance by 15% via root cause analysis to engineering machine learning pipelines achieving 0.91 ROC AUC. "
        f"Skilled at owning the analytics lifecycle end-to-end: relational database modeling, exploratory data analysis, dashboard development, "
        f"and business reporting directly aligned with the {job_title} requirements at {company}."
    )

    # 2. Re-order projects based on JD relevance
    project_scores = {}
    for p_key, p_data in PROJECT_BANK.items():
        score = sum(3 for kw in p_data["keywords"] if kw in desc)
        project_scores[p_key] = score
        
    ordered_project_keys = sorted(project_scores.keys(), key=lambda k: project_scores[k], reverse=True)
    ordered_projects = [PROJECT_BANK[k] for k in ordered_project_keys]

    # 3. Generate Overleaf / LaTeX CSS Styled HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Resume — Lokesh Pandey — {company} ({job_title})</title>
  <style>
    @page {{
      size: A4;
      margin: 14mm 16mm;
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Latin Modern Roman", "Computer Modern", "Times New Roman", Times, serif;
      font-size: 10pt;
      line-height: 1.35;
      color: #111111;
      background: #ffffff;
      padding: 20px 24px;
      max-width: 820px;
      margin: 0 auto;
    }}
    /* Overleaf Header */
    .header {{ text-align: center; margin-bottom: 12px; }}
    .name {{ font-size: 19pt; font-weight: bold; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 4px; }}
    .contact {{ font-size: 9pt; color: #333333; }}
    .contact a {{ color: #0b4578; text-decoration: none; }}
    .contact a:hover {{ text-decoration: underline; }}
    
    /* Section Headings (Overleaf standard rule) */
    .section-title {{
      font-size: 10.5pt;
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      border-bottom: 1px solid #222222;
      padding-bottom: 2px;
      margin-top: 12px;
      margin-bottom: 6px;
    }}
    
    /* Entries */
    .entry {{ margin-bottom: 7px; }}
    .entry-header {{ display: flex; justify-content: space-between; font-weight: bold; font-size: 9.5pt; }}
    .entry-sub {{ display: flex; justify-content: space-between; font-style: italic; font-size: 9pt; color: #444; margin-bottom: 2px; }}
    
    /* Bullet lists */
    ul {{ margin-left: 18px; margin-top: 2px; }}
    li {{ margin-bottom: 2.5px; font-size: 9pt; text-align: justify; }}
    
    .skills-table {{ width: 100%; border-collapse: collapse; font-size: 9pt; }}
    .skills-table td {{ padding: 2px 0; vertical-align: top; }}
    .skills-label {{ font-weight: bold; width: 155px; }}
    
    .tailor-badge {{
      display: inline-block;
      font-family: -apple-system, sans-serif;
      font-size: 7pt;
      background: #f0f4f8;
      border: 1px solid #c2d5e5;
      padding: 1px 6px;
      border-radius: 3px;
      color: #0b4578;
      margin-bottom: 8px;
    }}
  </style>
</head>
<body>

  <div style="text-align: right;">
    <span class="tailor-badge">TAILORED FOR: {company.upper()} // {job_title.upper()}</span>
  </div>

  <div class="header">
    <div class="name">LOKESH PANDEY</div>
    <div class="contact">
      Udham Singh Nagar, Uttarakhand | +91-9456382363 | <a href="mailto:pandeylokesh87@gmail.com">pandeylokesh87@gmail.com</a><br>
      <a href="https://linkedin.com/in/lokesh-pandey-2265b5218" target="_blank">linkedin.com/in/lokesh-pandey-2265b5218</a> | 
      <a href="{CANDIDATE_PROFILE['portfolio_url']}" target="_blank">lokesh-pandey-six.vercel.app</a> | 
      <a href="{CANDIDATE_PROFILE['github_url']}" target="_blank">github.com/Lokesh7-pqndey</a>
    </div>
  </div>

  <div class="section-title">Professional Summary</div>
  <p style="font-size: 9pt; text-align: justify; margin-bottom: 4px;">{summary}</p>

  <div class="section-title">Technical Skills</div>
  <table class="skills-table">
    <tr>
      <td class="skills-label">SQL & Databases:</td>
      <td>Advanced SQL, PostgreSQL, MySQL, Complex Joins, Subqueries, CTEs, Window Functions (NTILE, LAG/LEAD), Query Optimization</td>
    </tr>
    <tr>
      <td class="skills-label">Python & Analytics:</td>
      <td>Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, Exploratory Data Analysis (EDA), Statistical Modeling, Predictive ML</td>
    </tr>
    <tr>
      <td class="skills-label">Visualization & BI:</td>
      <td>Power BI (Star Schema, Advanced DAX Measures, Time-Intelligence, Interactive Dashboards), Advanced Excel (XLOOKUP, Pivot Tables)</td>
    </tr>
    <tr>
      <td class="skills-label">ERP & Operations:</td>
      <td>SAP ERP (Inventory Management, SKU velocity tracking), Root Cause Analysis, Cohort Retention, Churn Analytics</td>
    </tr>
  </table>

  <div class="section-title">Professional Experience</div>
  <div class="entry">
    <div class="entry-header">
      <span>Reliance Retail (Managed Services)</span>
      <span>Oct 2021 – Present</span>
    </div>
    <div class="entry-sub">
      <span>Department Manager — Data & Operations</span>
      <span>Rudrapur, Uttarakhand</span>
    </div>
    <ul>
      <li>Managed inventory movement and sales velocity across 1,000+ SKUs using SAP ERP, executing root-cause analysis that directly reduced stock variance by 15%.</li>
      <li>Built and automated multi-tab Excel reporting suites (advanced formulas, Pivot Tables, dynamic charts) for department leadership covering weekly and monthly KPIs and stock turns.</li>
      <li>Performed systematic data cleansing and cross-validation between SAP logs and spreadsheets to ensure 100% data integrity for procurement decisions.</li>
      <li>Collaborated with supply chain and category teams to define analytics requirements and translate raw operational data into strategic action plans.</li>
    </ul>
  </div>

  <div class="section-title">Key Analytics Projects</div>
"""

    for p in ordered_projects[:3]:
        html_content += f"""  <div class="entry">
    <div class="entry-header">
      <span>{p['title']}</span>
      <span>GitHub</span>
    </div>
    <div class="entry-sub">
      <span>Tech: {p['tech']}</span>
      <span></span>
    </div>
    <ul>
"""
        for b in p["bullets"]:
            html_content += f"      <li>{b}</li>\n"
        html_content += "    </ul>\n  </div>\n"

    html_content += f"""
  <div class="section-title">Certifications & Accreditations</div>
  <ul>
    <li><strong>Certified Data Science Professional</strong> — OdinSchool (Oct 2025 | Credential ID: <code>ODIN1005371</code>)</li>
    <li><strong>Data Analytics Job Simulation</strong> — Deloitte (Forage, 2025)</li>
    <li><strong>Introduction to Data for Decision Makers</strong> — Boston Consulting Group (BCG via Forage, 2025)</li>
    <li><strong>Markets Quantitative Analysis (MQA) Simulation</strong> — Forage (2025)</li>
  </ul>

  <div class="section-title">Education</div>
  <div class="entry">
    <div class="entry-header">
      <span>Swami Vivekanand Institute of Management Science & Technology</span>
      <span>2017 – 2020</span>
    </div>
    <div class="entry-sub">
      <span>Bachelor of Business Management (BBM) — GPA: 7.0/10</span>
      <span>India</span>
    </div>
  </div>

</body>
</html>
"""

    # Save tailored resume
    clean_company = "".join(c for c in company if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    res_path = RESUMES_DIR / f"resume_{clean_company}_{job_id}.html"
    with open(res_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {
        "resume_path": str(res_path),
        "resume_html": html_content
    }

def generate_tailored_cover_letter(job: Dict) -> Dict[str, str]:
    """
    Generates an Overleaf/LaTeX styled HTML & Markdown cover letter tailored for the specific company & role.
    """
    job_id = job.get("job_id", "job")
    job_title = job.get("title", "Data Analyst")
    company = job.get("company", "Company")
    reqs = job.get("requirements", "SQL, Python, Power BI, Advanced Excel")

    html_letter = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Cover Letter — Lokesh Pandey — {company} ({job_title})</title>
  <style>
    @page {{ size: A4; margin: 20mm 20mm; }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Latin Modern Roman", "Computer Modern", "Times New Roman", Times, serif;
      font-size: 10.5pt;
      line-height: 1.5;
      color: #111111;
      background: #ffffff;
      padding: 30px 36px;
      max-width: 800px;
      margin: 0 auto;
    }}
    .header {{ text-align: center; border-bottom: 1px solid #111; padding-bottom: 8px; margin-bottom: 24px; }}
    .name {{ font-size: 18pt; font-weight: bold; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 4px; }}
    .contact {{ font-size: 9.5pt; color: #333; }}
    .contact a {{ color: #0b4578; text-decoration: none; }}
    
    .recipient {{ margin-bottom: 20px; font-size: 10.5pt; }}
    .subject {{ font-weight: bold; text-decoration: underline; margin-bottom: 16px; font-size: 11pt; }}
    p {{ margin-bottom: 14px; text-align: justify; }}
    .bullets {{ margin-left: 20px; margin-bottom: 14px; }}
    .bullets li {{ margin-bottom: 6px; font-size: 10pt; }}
    .signature {{ margin-top: 24px; }}
  </style>
</head>
<body>

  <div class="header">
    <div class="name">LOKESH PANDEY</div>
    <div class="contact">
      Udham Singh Nagar, Uttarakhand | +91-9456382363 | <a href="mailto:pandeylokesh87@gmail.com">pandeylokesh87@gmail.com</a><br>
      Portfolio: <a href="{CANDIDATE_PROFILE['portfolio_url']}">lokesh-pandey-six.vercel.app</a> | 
      GitHub: <a href="{CANDIDATE_PROFILE['github_url']}">github.com/Lokesh7-pqndey</a>
    </div>
  </div>

  <div class="recipient">
    <strong>Date:</strong> 26 September 2026<br><br>
    <strong>Hiring Manager & Recruiting Team</strong><br>
    {company}<br>
  </div>

  <div class="subject">
    APPLICATION FOR: {job_title.upper()} (Req: {reqs})
  </div>

  <p>Dear Hiring Team at {company},</p>

  <p>
    I am writing to express my enthusiastic interest in the <strong>{job_title}</strong> role at <strong>{company}</strong>. 
    With 4+ years of hands-on business operations and data analytics experience at Reliance Retail, combined with comprehensive technical training 
    as a Certified Data Science Professional from OdinSchool, I have built a career translating complex relational databases and raw transaction logs into high-impact business decisions.
  </p>

  <p>
    Your job requirements emphasize <em>{reqs}</em>. Here is how my verified portfolio and production experience directly match what your team needs:
  </p>

  <ul class="bullets">
    <li><strong>Advanced SQL & Relational Database Engineering:</strong> Extensive experience writing complex multi-table joins, subqueries, and window functions (NTILE, LAG/LEAD, RANK, CTEs) in PostgreSQL and MySQL to discover structural bottlenecks and compensation models.</li>
    <li><strong>Predictive Analytics & Machine Learning (0.91 ROC AUC):</strong> In my Swiggy analytics project, I modeled 150K+ consumer orders and 100K users, engineering RFM behavioral features and deploying a Random Forest churn prediction classifier via a live Flask API.</li>
    <li><strong>Catalog Sourcing & Streaming EDA:</strong> Analyzed 6,200+ Netflix titles, resolving 2,445 missing metadata records and quantifying format mix (68% movies vs 32% TV shows) and TV-MA demographic dominance.</li>
    <li><strong>Institutional Business Intelligence (Power BI & DAX):</strong> Designed dimensional Star Schema architectures with custom dynamic DAX measures calculating Sharpe ratios, Alpha excess, and drawdown risk benchmarked against market indices.</li>
    <li><strong>Proven Business Impact at Scale:</strong> At Reliance Retail, I managed inventory across 1,000+ active SKUs in SAP ERP, leading root cause analysis that decreased stock variance by 15% and automating executive Excel KPI dashboards for department leadership.</li>
  </ul>

  <p>
    I am excited by the prospect of bringing this blend of technical analytical rigor and real-world operational ownership to {company}. 
    I invite you to review my live interactive portfolio and code repositories at <a href="{CANDIDATE_PROFILE['portfolio_url']}">{CANDIDATE_PROFILE['portfolio_url']}</a>.
  </p>

  <p>Thank you for your time and consideration. I welcome the opportunity to discuss how my skill set aligns with your team's immediate goals.</p>

  <div class="signature">
    Sincerely,<br><br>
    <strong>Lokesh Pandey</strong><br>
    Data Analyst & SQL Developer<br>
    +91-9456382363 | pandeylokesh87@gmail.com
  </div>

</body>
</html>
"""

    clean_company = "".join(c for c in company if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    letter_path = LETTERS_DIR / f"cover_letter_{clean_company}_{job_id}.html"
    with open(letter_path, "w", encoding="utf-8") as f:
        f.write(html_letter)

    return {
        "letter_path": str(letter_path),
        "letter_html": html_letter
    }
