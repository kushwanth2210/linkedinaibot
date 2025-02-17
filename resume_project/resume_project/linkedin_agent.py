import os
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
from models import LanguageModels  # Import LanguageModels from models.py
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from storage.gdrive import upload_to_google_drive  # Function to upload files to Google Drive

# Load environment variables
load_dotenv()

class LinkedInJobScraper:
    def __init__(self, model_name="claude-3-opus-20240229"):
        self.base_search_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        self.job_ids = []
        self.job_details = []
        
        # Initialize the Language Model
        self.language_model = LanguageModels(model=model_name).get_model()

    def fetch_job_ids(self, title, location, num_jobs=10):
        """Fetch job IDs from LinkedIn based on title and location."""
        title = title.replace(' ', '%20')
        location = location.replace(' ', '%20')
        start = 0
        
        while len(self.job_ids) < num_jobs:
            search_url = f"{self.base_search_url}?keywords={title}&location={location}&start={start}"
            response = requests.get(search_url)
            if response.status_code != 200:
                print(f"❌ Failed to fetch job listings: {response.status_code}")
                return
            
            list_soup = BeautifulSoup(response.text, "html.parser")
            page_jobs = list_soup.find_all("li")
            
            for job in page_jobs:
                base_card_div = job.find("div", {"class": "base-card"})
                if base_card_div:
                    job_entity_urn = base_card_div.get("data-entity-urn")
                    if job_entity_urn:
                        job_id = job_entity_urn.split(":")[-1]
                        if job_id not in self.job_ids:
                            self.job_ids.append(job_id)
                            if len(self.job_ids) >= num_jobs:
                                break
            start += 25  # Move to the next page
    
    def fetch_job_details(self, job_id):
        """Fetch job details for a given job ID."""
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        job_response = requests.get(job_url)
        
        if job_response.status_code != 200:
            print(f"❌ Failed to fetch job details for job ID {job_id}")
            return None
        
        soup = BeautifulSoup(job_response.text, 'html.parser')
        job_post = soup.get_text(separator='\n', strip=True)
        
        prompt_template = PromptTemplate(
            input_variables=["job_post"],
            template="""
            Extract all details from the job post, ensuring that every point and subpoint is preserved in a structured manner.

            **Extract the following:**
            1. **Company Information**: Name and brief description (if available).  
            2. **Job Details**: Role, date posted, employment type, location (remote/hybrid/on-site), and work authorization requirements.  
            3. **Job Summary**: High-level overview of the role and objectives.  
            4. **Key Responsibilities**: List all job duties and expectations with all the points included .  
            5. **Required Skills**: Technical and soft skills, education, certifications, and experience.  
            6. **Additional Details**: Salary, benefits, work schedule, and special/prefered requirements/qualifications.  
            7. **Application Process**: How to apply and recruiter contact details.  
            8. **Full Job Description**: Include the complete extracted text for reference.  

            **Job Post:**  
            {job_post}
            """
        )


        llm_chain = LLMChain(llm=self.language_model, prompt=prompt_template)
        response = llm_chain.run({"job_post": job_post})
        
        return {
            "Job ID": job_id,
            "Details": response
        }

    def save_to_json(self, data, filename="linkedin_job_details.json"):
        """Save job details locally and upload to Google Drive."""
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"✅ Saved job details locally: {filename}")
        
        # Upload to Google Drive
        try:
            file_id = upload_to_google_drive(filename)
            print(f"✅ Job details uploaded to Google Drive (File ID: {file_id})")
        except Exception as e:
            print(f"❌ Failed to upload job details to Google Drive: {str(e)}")

    def run(self):
        """Main function to fetch job details based on user input choice."""
        print("\nChoose an option:")
        print("1️⃣ Search for jobs by title and location")
        print("2️⃣ Enter a job ID manually")

        choice = input("Enter your choice (1/2): ").strip()

        if choice == "1":
            title = input("Enter job title: ").strip()
            location = input("Enter job location: ").strip()
            self.fetch_job_ids(title, location)

            if self.job_ids:
                job_id = self.job_ids[0]  # Fetch the first job ID from the list
                job_data = self.fetch_job_details(job_id)
                if job_data:
                    self.save_to_json(job_data)
            else:
                print("❌ No jobs found for the given criteria.")
        
        elif choice == "2":
            job_id = input("Enter the LinkedIn Job ID: ").strip()
            job_data = self.fetch_job_details(job_id)
            if job_data:
                self.save_to_json(job_data)
        else:
            print("❌ Invalid choice. Exiting...")

if __name__ == "__main__":
    scraper = LinkedInJobScraper()
    scraper.run()
