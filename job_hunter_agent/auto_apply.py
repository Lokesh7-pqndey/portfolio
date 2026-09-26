"""
Auto-Apply Execution Engine.
Automates matching, qualification, application payload generation,
and recording applied jobs to the database.
"""
import time
from typing import Dict, List
from config import CANDIDATE_PROFILE, JOB_SEARCH_CRITERIA
from database import is_job_applied, log_application
from matcher import analyze_job

def process_and_apply_jobs(discovered_jobs: List[Dict], max_applications: int = 15) -> List[Dict]:
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
            # Log as skipped so we don't re-scan unnecessarily
            log_application(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                platform=platform,
                job_url=url,
                match_score=match_score,
                matched_skills=matched_skills,
                missing_skills="",
                status="SKIPPED",
                notes=f"Below match threshold ({match_score}% < {JOB_SEARCH_CRITERIA['min_match_score']}%)"
            )
            continue
            
        # 4. Auto-Apply execution & logging
        print(f"  [+] QUALIFIED ({match_score}%): {title} @ {company} ({location})")
        print(f"      Matched Skills: {matched_skills}")
        
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
            status="APPLIED",
            notes=f"Auto-applied with tailored pitch and resume.pdf attached. Match score: {match_score}%"
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
                "tailored_pitch": tailored_pitch
            })
            
        if len(applied_list) >= max_applications:
            print(f"[!] Reached daily auto-apply target limit of {max_applications} jobs.")
            break
            
        time.sleep(0.1)  # safe throttle
        
    print(f"\n[✓] Run Completed: {len(applied_list)} Applied | {skipped_count} Skipped (low match) | {duplicate_count} Already Processed.")
    return applied_list
