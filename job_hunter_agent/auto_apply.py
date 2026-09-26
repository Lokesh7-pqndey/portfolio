"""
Auto-Apply Execution Engine.
Automates matching, qualification, application payload generation,
and recording applied jobs to the database.
"""
import sys
import time
from typing import Dict, List
from config import CANDIDATE_PROFILE, JOB_SEARCH_CRITERIA
from database import is_job_applied, log_application
from matcher import analyze_job
from resume_generator import generate_tailored_resume, generate_tailored_cover_letter
from live_submitter import attempt_live_submission

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def process_and_apply_jobs(discovered_jobs: List[Dict], max_applications: int = 40) -> List[Dict]:
    """
    Evaluates discovered jobs, filters out duplicates, applies to qualified jobs,
    and logs successful applications.
    """
    applied_list = []
    skipped_count = 0
    duplicate_count = 0
    
    print(f"\n[🚀] Processing {len(discovered_jobs)} discovered jobs...")
    
    for job in discovered_jobs:
        job_id = job["job_id"]
        title = job["title"]
        company = job["company"]
        location = job.get("location", "India")
        platform = job.get("platform", "LinkedIn")
        url = job.get("job_url", "")
        desc = job.get("description", "")
        
        # 1. Skip if already applied
        if is_job_applied(job_id):
            duplicate_count += 1
            continue
            
        # 2. Analyze job match
        analysis = analyze_job(title, desc)
        match_score = analysis["match_score"]
        matched_skills = analysis["matched_skills_str"]
        tailored_pitch = analysis["tailored_pitch"]
        
        # 3. Check qualification threshold
        if not analysis["is_qualified"]:
            skipped_count += 1
            continue
            
        reqs = job.get("requirements", "")

        # 4. Generate Dynamic Overleaf Tailored Resume & Matching Cover Letter
        res_info = generate_tailored_resume(job)
        letter_info = generate_tailored_cover_letter(job)
        tailored_resume_path = res_info["resume_path"]
        cover_letter_path = letter_info["letter_path"]

        # 5. Auto-Apply execution & Live Submission
        print(f"  [+] QUALIFIED ({match_score}%): [{platform}] {title} @ {company} ({location})")
        print(f"      Requirements: {reqs}")
        print(f"      📄 Tailored Overleaf Resume: {tailored_resume_path}")
        print(f"      ✉️ Tailored Cover Letter:    {cover_letter_path}")
        
        # Real browser form fill & live submission attempt
        live_result = attempt_live_submission(job)
        live_status = live_result.get("status", "APPLIED")
        live_notes = f"{live_result.get('message', '')} | Match: {match_score}%"
        proof_path = live_result.get("proof_screenshot", "")
        if proof_path:
            live_notes += f" | Proof: {proof_path}"
        
        success = log_application(
            job_id=job_id,
            title=title,
            company=company,
            location=location,
            platform=platform,
            job_url=url,
            match_score=match_score,
            matched_skills=matched_skills,
            missing_skills="",
            status=live_status,
            notes=live_notes,
            requirements=reqs,
            tailored_resume_path=tailored_resume_path,
            cover_letter_path=cover_letter_path
        )
        
        if success:
            applied_list.append({
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "platform": platform,
                "url": url,
                "match_score": match_score,
                "matched_skills": matched_skills,
                "requirements": reqs,
                "tailored_pitch": tailored_pitch,
                "tailored_resume_path": tailored_resume_path,
                "cover_letter_path": cover_letter_path
            })
            
        if len(applied_list) >= max_applications:
            print(f"[!] Reached daily auto-apply target limit of {max_applications} jobs.")
            break
            
        time.sleep(0.1)  # safe throttle
        
    print(f"\n[✓] Run Completed: {len(applied_list)} Applied | {skipped_count} Skipped (low match) | {duplicate_count} Already Processed.")
    return applied_list
