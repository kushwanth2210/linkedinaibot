import os
import subprocess
from dotenv import load_dotenv
from pdflatex import PDFLaTeX

# Load environment variables
load_dotenv()

class ResumeGenerator:
    def __init__(self, output_filename="resume"):
        self.output_filename = output_filename
        self.personal_info = {}
        self.skills = []
        self.work_experience = []
        self.education = []
        self.certifications = []
        self.projects = []

    def set_personal_info(self, name, location, phone, email, linkedin, github):
        self.personal_info = {
            "name": name,
            "location": location,
            "phone": phone,
            "email": email,
            "linkedin": linkedin,
            "github": github
        }

    def add_skill(self, category, skills_list):
        self.skills.append((category, skills_list))

    def add_work_experience(self, company, location, position, date_range, responsibilities):
        self.work_experience.append({
            "company": company,
            "location": location,
            "position": position,
            "date_range": date_range,
            "responsibilities": responsibilities
        })

    def add_education(self, institution, location, degree, gpa, date_range):
        self.education.append({
            "institution": institution,
            "location": location,
            "degree": degree,
            "gpa": gpa,
            "date_range": date_range
        })

    def add_certification(self, certification_name, institution, date):
        self.certifications.append({
            "certification_name": certification_name,
            "institution": institution,
            "date": date
        })

    def add_project(self, project_name, technologies, description, date):
        self.projects.append({
            "project_name": project_name,
            "technologies": technologies,
            "description": description,
            "date": date
        })

    def generate_latex(self):
        latex_content = f"""
        \documentclass[letterpaper,10pt]{{article}}
        \usepackage{{hyperref}}
        \begin{{document}}
        \begin{{center}}
        \textbf{{\Large {self.personal_info.get('name', '')}}} \\
        {self.personal_info.get('location', '')} | {self.personal_info.get('phone', '')} | \href{{mailto:{self.personal_info.get('email', '')}}}{{{self.personal_info.get('email', '')}}} | \href{{{self.personal_info.get('linkedin', '')}}}{{LinkedIn}} | \href{{{self.personal_info.get('github', '')}}}{{GitHub}}
        \end{{center}}

        \section*{{Skills}}
        \begin{{itemize}}
        """
        for category, skills_list in self.skills:
            latex_content += f"\item \textbf{{{category}}}: {', '.join(skills_list)}\n"
        
        latex_content += "\end{itemize}\n\section*{Work Experience}\n"
        for exp in self.work_experience:
            latex_content += f"\textbf{{{exp['company']}}} ({exp['location']}) \\\ \textit{{{exp['position']}}} ({exp['date_range']})\n\begin{{itemize}}"
            for res in exp['responsibilities']:
                latex_content += f"\item {res}\n"
            latex_content += "\end{itemize}"
        
        latex_content += "\section*{Education}\n"
        for edu in self.education:
            latex_content += f"\textbf{{{edu['institution']}}} ({edu['location']}) \\\ \textit{{{edu['degree']}}}, GPA: {edu['gpa']} ({edu['date_range']})\n"
        
        latex_content += "\section*{Certifications}\begin{itemize}\n"
        for cert in self.certifications:
            latex_content += f"\item {cert['certification_name']} - {cert['institution']} ({cert['date']})\n"
        latex_content += "\end{itemize}\n"
        
        latex_content += "\section*{Projects}\n"
        for proj in self.projects:
            latex_content += f"\textbf{{{proj['project_name']}}} ({proj['date']}) \\\ \textit{{{proj['technologies']}}}\n\begin{{itemize}}"
            latex_content += f"\item {proj['description']}\n"
            latex_content += "\end{itemize}"
        
        latex_content += "\end{document}"
        return latex_content

    def save_as_tex(self):
        tex_filename = f"{self.output_filename}.tex"
        with open(tex_filename, "w") as f:
            f.write(self.generate_latex())
        print(f"LaTeX file saved: {tex_filename}")

    def save_as_pdf(self):
        self.save_as_tex()
        pdfl = PDFLaTeX.from_texfile(f"{self.output_filename}.tex")
        pdf, _, _ = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
        print(f"PDF generated: {self.output_filename}.pdf")
        return pdf

if __name__ == "__main__":
    resume = ResumeGenerator("resume")
    resume.set_personal_info("John Doe", "New York, NY", "+1 123 456 7890", "johndoe@email.com", "https://linkedin.com/in/johndoe", "https://github.com/johndoe")
    resume.add_skill("Programming", ["Python", "JavaScript", "SQL"])
    resume.add_work_experience("Company A", "New York", "Software Engineer", "Jan 2020 - Present", ["Developed APIs", "Led a team of developers"])
    resume.add_education("XYZ University", "New York", "B.S. in Computer Science", "3.8/4.0", "2015 - 2019")
    resume.add_project("Portfolio Website", "React, Node.js", "Developed a personal portfolio website", "2021")
    resume.save_as_pdf()
