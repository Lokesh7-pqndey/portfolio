"""
Lokesh's Autonomous Job Hunter & Application Agent.
Main CLI command center.

Usage:
  python main.py run           # Scan, match, auto-apply, and generate today's report
  python main.py report        # Display today's application report
  python main.py match "JD"    # Test match score on any custom Job Description
  python main.py schedule      # Run automatically every day at 09:00 AM
"""
import sys
import os
import io
import time

# Ensure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from scraper import discover_all_jobs
from auto_apply import process_and_apply_jobs
from reporter import generate_daily_report, print_daily_summary
from matcher import analyze_job

def run_job_hunt():
    """Executes the full discovery -> match -> apply -> report cycle."""
    print("=" * 70)
    print("🚀 STARTING AUTONOMOUS JOB APPLICATION AGENT")
    print("Candidate: Lokesh Pandey — Data Analyst & SQL Developer")
    print("=" * 70)
    
    # 1. Discover jobs
    jobs = discover_all_jobs()
    
    # 2. Process, match, and apply
    process_and_apply_jobs(jobs, max_applications=40)
    
    # 3. Generate and display daily report
    print_daily_summary()

def run_scheduled():
    """Runs the job hunter on a recurring daily schedule."""
    import schedule
    
    print("[*] Scheduler active. Job Hunter Agent will run automatically daily at 09:00 AM.")
    print("    Press Ctrl+C to stop.")
    
    # Run once immediately on start
    run_job_hunt()
    
    # Schedule for 09:00 AM daily
    schedule.every().day.at("09:00").do(run_job_hunt)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    if len(sys.argv) < 2:
        command = "run"
    else:
        command = sys.argv[1].lower()
        
    if command == "run":
        run_job_hunt()
    elif command == "report":
        print_daily_summary()
    elif command == "login":
        from live_submitter import launch_persistent_login_window
        launch_persistent_login_window()
    elif command == "schedule":
        run_scheduled()
    elif command == "match":
        test_text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Data Analyst requiring SQL, Python, Power BI"
        res = analyze_job("Test Role", test_text)
        print(f"\nMatch Score: {res['match_score']}%")
        print(f"Qualified: {res['is_qualified']}")
        print(f"Matched Skills: {res['matched_skills_str']}\n")
    else:
        print(f"Unknown command '{command}'. Available: run, report, login, schedule, match")

if __name__ == "__main__":
    main()
