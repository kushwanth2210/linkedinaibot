import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

class ResumeUpdater:
    def __init__(self):
        """
        Initialize the ResumeUpdater class with the Anthropic API key.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API Key is missing. Please check your .env file.")

        self.llm = ChatAnthropic(
            model_name="claude-3-opus-20240229",
            anthropic_api_key=api_key
        )
        self.prompt_template = PromptTemplate(
            input_variables=["job_details", "latex_resume"],
            template="""
            You are an AI that updates resumes in LaTeX format for a specific job position.
            
            Job Description:
            {job_details}
            
            Existing LaTeX Resume:
            {latex_resume}
            
            Update the resume to highlight relevant skills, work experience, and projects to align with the job description.
            
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
        
        if not job_details or not latex_resume:
            raise ValueError("Job details and LaTeX resume must not be empty.")
        
        updated_latex_resume = self.chain.run({"job_details": job_details, "latex_resume": latex_resume})
        return updated_latex_resume

if __name__ == "__main__":
    def get_job_details():
        """
        This function should return job details from an external source (e.g., database, API, or input).
        """
        return "Software Engineer role at XYZ Corp, focusing on Python and Machine Learning."

    def get_latex_resume():
        """
        This function should return the existing LaTeX resume from an external source.
        """
        return "\documentclass{article} ... \end{document}"  # Placeholder

    resume_updater = ResumeUpdater()
    updated_resume = resume_updater.update_resume(get_job_details, get_latex_resume)
    
    print("Updated LaTeX Resume:")
    print(updated_resume)
