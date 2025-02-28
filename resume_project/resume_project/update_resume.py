import os
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from scripts.models import LanguageModels
from ats_evaluation import ATSAnalyzer
from update_resume import find_job_section, update_job_description, compile_to_pdf
from resume_creation import JinjaLatexResume
from storage.gdrive import GoogleDriveHandler

# Initialize AI Model from models.py
language_model = LanguageModels(model="gpt-4").get_model()

# Initialize Google Drive Handler
gdrive_handler = GoogleDriveHandler()


# Resume State Class for LangGraph
class ResumeState:
    def __init__(self, latex_resume, job_description):
        self.latex_resume = latex_resume  # LaTeX resume content
        self.job_description = job_description  # Job description content
        self.keywords = []
        self.missing_keywords = []
        self.updated_experience = []
        self.updated_skills = []
        self.final_resume = None


# Step 1: Extract Keywords from Job Description
def extract_keywords(state):
    print("🔍 Extracting Keywords from Job Description...")
    ats_analyzer = ATSAnalyzer(state.job_description, state.latex_resume)
    keywords = ats_analyzer.get_ats_score()  # Extract important words
    state.keywords = keywords
    return state


# Step 2: Identify Missing Keywords in the Resume
def find_missing_keywords(state):
    print("🔎 Identifying missing keywords in resume...")
    resume_text = open(state.latex_resume, "r").read()
    state.missing_keywords = [kw for kw in state.keywords if kw.lower() not in resume_text.lower()]
    return state


# Step 3: Enhance Work Experience Section
def enhance_work_experience(state):
    print("📝 Enhancing work experience with missing keywords...")

    with open(state.latex_resume, "r") as f:
        lines = f.readlines()

    start_idx, end_idx = find_job_section(lines, "Work Experience")  # Locate section
    work_experience = lines[start_idx:end_idx + 1]

    # AI-powered Work Experience Enhancement
    prompt = PromptTemplate(
        input_variables=["experience", "keywords"],
        template="Revise this work experience:\n{experience}\nInclude the following keywords professionally: {keywords}"
    )

    chain = LLMChain(llm=language_model, prompt=prompt)
    new_experience = chain.run({"experience": work_experience, "keywords": state.missing_keywords})

    state.updated_experience = new_experience.split("\n")
    state.latex_resume = update_job_description(lines, start_idx, end_idx, state.updated_experience)

    return state


# Step 4: Add Missing Skills
def add_missing_skills(state):
    print("📌 Adding missing skills...")

    with open(state.latex_resume, "r") as f:
        resume_text = f.read()

    skill_section_match = re.search(r"\\section\*{Skills}([\s\S]*?)\\section", resume_text)
    existing_skills = skill_section_match.group(1) if skill_section_match else ""

    new_skills = [kw for kw in state.missing_keywords if kw not in existing_skills]

    if new_skills:
        skill_text = "\n".join([f"\\item {skill}" for skill in new_skills])
        state.updated_skills = skill_text
        resume_text = resume_text.replace(existing_skills, existing_skills + "\n" + skill_text)

        with open(state.latex_resume, "w") as f:
            f.write(resume_text)

    return state


# Step 5: Improve Grammar and Readability
def improve_grammar(state):
    print("📖 Enhancing grammar and readability...")

    with open(state.latex_resume, "r") as f:
        resume_text = f.read()

    # AI-powered text refinement
    prompt = PromptTemplate(
        input_variables=["resume"],
        template="Improve the grammar and professionalism of this resume: {resume}"
    )

    chain = LLMChain(llm=language_model, prompt=prompt)
    refined_resume = chain.run({"resume": resume_text})

    with open(state.latex_resume, "w") as f:
        f.write(refined_resume)

    state.final_resume = state.latex_resume
    return state


# Step 6: Compile Resume and Upload to Google Drive
def save_to_gdrive(state):
    print("☁️ Saving updated resume to Google Drive...")

    pdf_filename = state.final_resume.replace(".tex", ".pdf")
    compile_to_pdf(state.final_resume)

    file_id = gdrive_handler.upload_file(pdf_filename, "Updated_Resume.pdf")
    print(f"✅ Resume uploaded to Google Drive (File ID: {file_id})")

    return state


# Constructing the optimized LangGraph workflow
workflow = StateGraph(ResumeState)

# Adding Nodes (Each Step)
workflow.add_node("extract_keywords", extract_keywords)
workflow.add_node("find_missing_keywords", find_missing_keywords)
workflow.add_node("enhance_work_experience", enhance_work_experience)
workflow.add_node("add_missing_skills", add_missing_skills)
workflow.add_node("improve_grammar", improve_grammar)
workflow.add_node("save_to_gdrive", save_to_gdrive)

# Define edges for optimized parallel execution
workflow.add_edge("extract_keywords", "find_missing_keywords")
workflow.add_edge("find_missing_keywords", "enhance_work_experience")
workflow.add_edge("find_missing_keywords", "add_missing_skills")  # Parallel execution
workflow.add_edge("enhance_work_experience", "improve_grammar")
workflow.add_edge("add_missing_skills", "improve_grammar")  # Parallel execution
workflow.add_edge("improve_grammar", "save_to_gdrive")

workflow.set_entry_point("extract_keywords")
workflow.set_termination_nodes("save_to_gdrive")

# Running the Workflow
def run_resume_update(latex_resume, job_description):
    initial_state = ResumeState(latex_resume, job_description)
    final_state = workflow.run(initial_state)
    return final_state


# Example Usage
if __name__ == "__main__":
    latex_resume_path = "resume.tex"
    job_description_text = open("job_description.txt", "r").read()

    print("🚀 Starting Resume Update Process...")
    run_resume_update(latex_resume_path, job_description_text)
