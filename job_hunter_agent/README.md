# 🤖 Lokesh's Autonomous Job Hunter & Application Agent

An automated job search, matching, and application agent built specifically for **Lokesh Pandey** (Data Analyst & SQL Developer).

---

## ⚡ What This Agent Does Automatically

1. **Auto-Discovery:** Scrapes real active job openings for *Data Analyst*, *SQL Developer*, and *Power BI Developer* roles across LinkedIn and job networks.
2. **Intelligent Profile Matching:** Analyzes job descriptions and calculates match scores (0–100%) against Lokesh's core skills (PostgreSQL, Python, Power BI, DAX, Excel, SAP, Machine Learning).
3. **Application & Tailored Pitches:** Automatically qualifies jobs (≥65% match), generates role-tailored cover notes, links the live portfolio & resume, and logs applications to an SQLite database (`applications.db`).
4. **Duplicate Prevention:** Ensures you never apply to the same job twice.
5. **Daily Intelligence Reports:** Generates structured daily markdown reports in `reports/daily_report_YYYY-MM-DD.md` summarizing all applied jobs, match scores, company names, and direct links.

---

## 🚀 Quick Start & Commands

Navigate to the agent directory:
```bash
cd "job_hunter_agent"
```

### 1. Run Today's Job Hunt & Apply
```bash
python main.py run
```
*Discovers active jobs, applies to top qualified matches, and generates today's report.*

### 2. View Today's Applied Jobs Report
```bash
python main.py report
```
*Displays the markdown table of all jobs applied today.*

### 3. Test Match on any Job Description
```bash
python main.py match "Looking for Data Analyst with SQL, Python, Power BI, and 3+ years experience"
```

### 4. Run Daily Scheduler (Automatic 09:00 AM)
```bash
python main.py schedule
```

---

## 📁 Architecture & Files

- `config.py`: Candidate profile (Email, Phone, Portfolio, Resume path, CTC, Notice period) and search criteria.
- `database.py`: SQLite tracking database (`applications.db`) storing applied jobs and metrics.
- `matcher.py`: Skill weight matrix, qualification logic, and tailored cover pitch generator.
- `scraper.py`: Public job discovery across LinkedIn and remote feeds.
- `auto_apply.py`: Application execution and rate-limiting.
- `reporter.py`: Daily report generator saving reports to `reports/`.
- `main.py`: Unified CLI command center.
