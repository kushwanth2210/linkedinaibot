import os
from dotenv import load_dotenv
from resume_update import ResumeUpdater
from ats_evaluation import ATSAnalyzer
from linkedin_agent import LinkedInJobScraper

# Load environment variables
load_dotenv()

def run_resume_update():
    """Run the resume update process."""
    def get_job_details():
        return input("Enter job details: ")
    
    def get_latex_resume():
        return input("Enter existing LaTeX resume content: ")
    
    updater = ResumeUpdater()
    updated_resume = updater.update_resume(get_job_details, get_latex_resume)
    print("Updated Resume:")
    print(updated_resume)


def run_ats_evaluation():
    """Run the ATS evaluation process."""
    job_description = input("Enter job description: ")
    resume_path = input("Enter path to resume PDF: ")
    
    ats = ATSAnalyzer(job_description, resume_path)
    score = ats.get_ats_score()
    
    if score is not None:
        print(f"ATS Match Score: {score}%")
        if score >= 75:
            print("✅ Resume is well-matched to the job. Good to apply!")
        elif 50 <= score < 75:
            print("⚠️ Resume is somewhat relevant, but improvements are recommended.")
        else:
            print("❌ Resume is a poor match. Consider tailoring it to the job description.")


def run_linkedin_scraper():
    """Run the LinkedIn job scraper."""
    title = input("Enter job title: ")
    location = input("Enter job location: ")
    
    scraper = LinkedInJobScraper(title, location)
    scraper.run()
    print("Job scraping completed. Results saved to linkedin_job_details.json")

if __name__ == "__main__":
    print("Select an option:")
    print("1. Update Resume")
    print("2. Run ATS Evaluation")
    print("3. Scrape LinkedIn Jobs")
    
    choice = input("Enter choice (1/2/3): ")
    
    if choice == "1":
        run_resume_update()
    elif choice == "2":
        run_ats_evaluation()
    elif choice == "3":
        run_linkedin_scraper()
    else:
        print("Invalid choice.")
