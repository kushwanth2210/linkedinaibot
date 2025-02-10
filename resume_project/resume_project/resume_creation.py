import os
import subprocess
from pdflatex import PDFLaTeX

class ResumeGenerator:
    def __init__(self):
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
        latex_content = r"""
        \documentclass[letterpaper,8pt]{article}
        \usepackage{fancyhdr, titlesec, enumitem, hyperref, tabularx, ragged2e}
        \pagestyle{fancy}
        \fancyhf{}
        \renewcommand{\headrulewidth}{0pt}
        \renewcommand{\footrulewidth}{0pt}

        \begin{document}
        \begin{center}
        {\huge \scshape %s} \\ 
        {\small %s | %s | \href{mailto:%s}{%s} | \href{%s}{LinkedIn} | \href{%s}{GitHub}}
        \end{center}

        \section*{Skills}
        \begin{itemize}
        """ % (self.personal_info.get("name", ""), self.personal_info.get("location", ""), 
               self.personal_info.get("phone", ""), self.personal_info.get("email", ""), 
               self.personal_info.get("email", ""), self.personal_info.get("linkedin", ""), 
               self.personal_info.get("github", ""))

        for category, skills_list in self.skills:
            latex_content += r"\item \textbf{%s}: %s" % (category, ', '.join(skills_list))

        latex_content += r"\end{itemize}"

        latex_content += r"\section*{Work Experience}"
        for exp in self.work_experience:
            latex_content += r"\textbf{%s} (%s) \\ \textit{%s} (%s)" % (exp['company'], exp['location'], exp['position'], exp['date_range'])
            latex_content += r"\begin{itemize}"
            for res in exp['responsibilities']:
                latex_content += r"\item %s" % res
            latex_content += r"\end{itemize}"

        latex_content += r"\section*{Education}"
        for edu in self.education:
            latex_content += r"\textbf{%s} (%s) \\ \textit{%s}, GPA: %s (%s)" % (edu['institution'], edu['location'], edu['degree'], edu['gpa'], edu['date_range'])

        latex_content += r"\section*{Certifications}"
        for cert in self.certifications:
            latex_content += r"\item %s - %s (%s)" % (cert['certification_name'], cert['institution'], cert['date'])

        latex_content += r"\section*{Projects}"
        for proj in self.projects:
            latex_content += r"\textbf{%s} (%s) \\ \textit{%s}" % (proj['project_name'], proj['date'], proj['technologies'])
            latex_content += r"\begin{itemize}"
            latex_content += r"\item %s" % proj['description']
            latex_content += r"\end{itemize}"

        latex_content += r"\end{document}"

        return latex_content

    def save_as_tex(self, output_filename="resume.tex"):
        latex_code = self.generate_latex()
        with open(output_filename, "w") as f:
            f.write(latex_code)
        print(f"LaTeX file saved successfully: {output_filename}")

    def save_as_pdf(self, output_filename="resume.pdf"):
        self.save_as_tex()  # Save the .tex file before generating the PDF
        tex_filename = "resume.tex"

        try:
            subprocess.run(["pdflatex", tex_filename], check=True)
            os.rename("resume.pdf", output_filename)
            print(f"PDF generated successfully: {output_filename}")
        except subprocess.CalledProcessError as e:
            print("Error occurred while generating PDF:", e)
        finally:
            # Clean up auxiliary files generated by pdflatex
            for ext in ["aux", "log", "out"]:
                if os.path.exists(f"resume.{ext}"):
                    os.remove(f"resume.{ext}")

    def process_file(self):
        pdfl = PDFLaTeX.from_texfile('resume.tex')
        pdf, log, completed_process = pdfl.create_pdf(
            keep_pdf_file=True, 
            keep_log_file=True
        )

        # Rename the generated PDF file to match the expected output
        if os.path.exists('resume.pdf'):
            os.rename('resume.pdf', 'Kushwanth_Resume.pdf')
            print("PDF processed and renamed successfully as Kushwanth_Resume.pdf")
        else:
            print("PDF generation failed. 'resume.pdf' not found.")

        return pdf



resume = ResumeGenerator()
resume.set_personal_info("Kushwanth Kumar Karamsetti", "Dallas, TX", "+1 (929) 361-8554", "kkushwanth77@gmail.com", "https://www.linkedin.com/in/kushwanthkaramsetti/", "https://github.com/kushwanth2210")

resume.add_skill("Programming Languages", ["Python", "SQL", "Java", "Pyspark", "Linux"])
resume.add_skill("Cloud Platforms and DevOps", ["AWS", "Azure", "Docker", "Kubernetes", "Terraform", "Datadog", "Amazon Bedrock", "Git", "GitHub", "SSH", "Harness", "Jenkins", "Snowflake", "Apache Airflow", "Azure Data Factory (ADF)", "AWS Sagemaker", "Databricks", "Oracle SQL", "MongoDB Atlas", "PostgreSQL", "SQL Server", "Kafka", "Pandas", "PowerBI"])
resume.add_skill("Machine Learning", ["PyTorch", "TensorFlow", "Scikit-learn", "Regression", "Hypothesis Testing", "Feature Engineering", "Model Deployment", "Workflow Automation", "Model Monitoring", "Model Drift Detection", "Data Drift Detection"])
resume.add_skill("Generative AI", ["OpenCV", "Deep Learning", "NLP", "Fine-tuning LLMs", "Medical Imaging", "RAG Implementation", "Hugging Face", "Vector Databases", "Embedding Models", "Prompting Techniques", "Speech Recognition (Whisper AI)", "Azure AI Studio", "Langchain", "LangGraph", "LlamaIndex", "Haystack", "Vertex AI"])

resume.add_work_experience("Tror - AI for Everyone", "Nashville, Tennessee", "Senior Data Scientist", "Dec 2022 - Present", ["Developed Generative AI chat agents", "Integrated AI chatbots", "Optimized AI workflows"])
resume.add_work_experience("Kimberly-Clark", "Bangalore, India", "Data Engineer", "May 2022 - Dec 2022", ["Managed data pipelines", "Improved data transformations"])
resume.add_work_experience("Tror - AI for Everyone", "Hyderabad, India", "Data Scientist Intern", "May 2021 - May 2022", ["Contributed to MDM workflows", "Worked on lung cancer detection"])

resume.add_education("Webster University", "San Antonio, TX", "Masters in IT Management", "3.93/4.0", "Sep 2023 - Dec 2024")
resume.add_education("NIT Surat", "Surat, India", "B.Tech in Mechanical Engineering", "8.02/10.0", "Jul 2018 - May 2022")

resume.add_project("Leaf Disease Detection", "Python, Flask", "Developed CNN model for detecting leaf diseases", "2022")
resume.add_project("Autonomous Object Detection", "OpenCV, YOLOv5", "Built real-time object detection system", "2022")
resume.add_project("Image Classification", "TensorFlow, Keras", "Multi-class image classification with high accuracy", "2021")

# Save as TeX
resume.save_as_tex("Kushwanth_Resume.tex")

# Save as PDF
resume.save_as_pdf("Kushwanth_Resume.pdf")

# Alternatively, process using pdflatex
resume.process_file()
