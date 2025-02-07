import os
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class ResumeUpdater:
    def __init__(self, api_key):
        """
        Initialize the ResumeUpdater class with the Anthropic API key.
        """
        self.llm = ChatAnthropic(
            model_name="claude-3-opus-20240229",
            anthropic_api_key=api_key
        )
        self.prompt_template = PromptTemplate(
            input_variables=["job_details", "latex_resume"],
            template="""
            You are an AI that updates resumes in LaTeX format for a specific job position.

            Here is the job description:
            {job_details}

            Here is the existing LaTeX resume:
            {latex_resume}

            Update the LaTeX resume to highlight the relevant skills, work experience, and projects to align with the job description. Ensure the formatting remains correct and professional.

            Return only the updated LaTeX code.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def update_resume(self, job_details_func, latex_resume_func):
        """
        Updates the LaTeX resume based on the job details.
        job_details_func: Function that returns job details as a string.
        latex_resume_func: Function that returns the existing LaTeX resume as a string.
        """
        job_details = job_details_func()
        latex_resume = latex_resume_func()
        
        updated_latex_resume = self.chain.run({"job_details": job_details, "latex_resume": latex_resume})
        return updated_latex_resume

# Example functions to fetch job details and LaTeX resume (to be implemented elsewhere)
def get_job_details():
    """
    This function should return job details from an external source (e.g., database, API, or input).
    """
    return "TO BE ENTERED"

def get_latex_resume():
    """
    This function should return the LaTeX resume from an external source.
    """
    return "TO BE ENTERED"

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("ANTHROPIC_API_KEY")  # Ensure the API key is set in the environment
    resume_updater = ResumeUpdater(api_key)
    updated_resume = resume_updater.update_resume(get_job_details, get_latex_resume)
    
    print(updated_resume)  # Output the updated LaTeX resume
