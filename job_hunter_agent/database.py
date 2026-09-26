"""
Database manager for the Autonomous Job Hunter Agent.
Handles recording applied jobs, preventing duplicates, and querying daily statistics.
"""
import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applied_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT,
        platform TEXT DEFAULT 'LinkedIn',
        job_url TEXT,
        match_score REAL,
        matched_skills TEXT,
        missing_skills TEXT,
        requirements TEXT,
        tailored_resume_path TEXT,
        cover_letter_path TEXT,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'APPLIED',
        application_notes TEXT
    )
    """)
    # Migration check for existing database
    for col in ["requirements", "tailored_resume_path", "cover_letter_path"]:
        try:
            cursor.execute(f"ALTER TABLE applied_jobs ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()

def is_job_applied(job_id: str) -> bool:
    """Checks whether this job has already been successfully applied to."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM applied_jobs WHERE job_id = ? AND status = 'APPLIED'", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def log_application(
    job_id: str,
    title: str,
    company: str,
    location: str,
    platform: str,
    job_url: str,
    match_score: float,
    matched_skills: str,
    missing_skills: str,
    status: str = "APPLIED",
    notes: str = "",
    requirements: str = "",
    tailored_resume_path: str = "",
    cover_letter_path: str = ""
) -> bool:
    """Logs a newly applied job into the database with tailored resume and cover letter paths."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO applied_jobs (
            job_id, title, company, location, platform, job_url, 
            match_score, matched_skills, missing_skills, requirements,
            tailored_resume_path, cover_letter_path, applied_at, status, application_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_id, title, company, location, platform, job_url,
            match_score, matched_skills, missing_skills, requirements,
            tailored_resume_path, cover_letter_path,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status, notes
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_today_applied_jobs() -> List[Dict]:
    """Returns all jobs applied on the current date."""
    conn = get_connection()
    cursor = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT * FROM applied_jobs 
        WHERE date(applied_at) = ? AND status = 'APPLIED'
        ORDER BY applied_at DESC
    """, (today_str,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_overall_stats() -> Dict:
    """Returns high-level application statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    
    cursor.execute("SELECT COUNT(*) FROM applied_jobs WHERE status = 'APPLIED'")
    total_applied = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM applied_jobs WHERE date(applied_at) = ? AND status = 'APPLIED'", (today_str,))
    today_applied = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(match_score) FROM applied_jobs WHERE status = 'APPLIED'")
    avg_match = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return {
        "total_applied": total_applied,
        "today_applied": today_applied,
        "average_match_score": round(avg_match, 1)
    }

# Run init on import
init_db()
