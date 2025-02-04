import requests
from bs4 import BeautifulSoup
import json
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class LinkedInJobScraper:
    def __init__(self, title, location, api_key, num_jobs=10):
        self.title = title.replace(' ', '%20')
        self.location = location.replace(' ', '%20')
        self.base_search_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        self.job_ids = []
        self.job_details = []
        self.num_jobs = num_jobs  # Number of jobs to fetch

        # Initialize the Anthropic model
        self.llm = ChatAnthropic(
            model_name="claude-3-opus-20240229",
            anthropic_api_key=api_key
        )

    def fetch_job_ids(self):
        start = 0
        while len(self.job_ids) < self.num_jobs:
            search_url = f"{self.base_search_url}?keywords={self.title}&location={self.location}&start={start}"
            response = requests.get(search_url)
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
                            if len(self.job_ids) >= self.num_jobs:
                                break

            start += 25  # Move to the next page

    def fetch_job_details(self):
        for job_id in self.job_ids:
            job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
            job_response = requests.get(job_url)
            soup = BeautifulSoup(job_response.text, 'html.parser')

            job_description = soup.get_text(separator='\n', strip=True)

            # LLM Prompt Template
            prompt_template = PromptTemplate(
                input_variables=["job_description"],
                template="""
                Extract the following information from the job description:
                1. **Company Name**
                2. **Date Posted**
                3. **Role**
                4. **Key Responsibilities**
                5. **Required Skills**
                6. **About the Company**

                Job Description:
                {job_description}
                """
            )

            llm_chain = LLMChain(llm=self.llm, prompt=prompt_template)
            response = llm_chain.run({"job_description": job_description})

            self.job_details.append({
                "Job ID": job_id,
                "Details": response
            })

    def save_to_json(self, filename="linkedin_job_details.json"):
        with open(filename, 'w') as json_file:
            json.dump(self.job_details, json_file, indent=4)

    def run(self):
        self.fetch_job_ids()
        self.fetch_job_details()
        self.save_to_json()

# Example usage
if __name__ == "__main__":
    api_key = 'api_key'
    scraper = LinkedInJobScraper(title="Python Developer", location="United States", api_key=api_key)
    scraper.run()

