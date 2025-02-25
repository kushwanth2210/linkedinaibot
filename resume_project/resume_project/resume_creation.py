import os
import shutil
from jinja2 import Environment
from pdflatex import PDFLaTeX
from storage.gdrive import GoogleDriveHandler  # Ensure your GoogleDriveHandler is correctly imported
from templates.latex_template import tex_template_content

# Custom Jinja2 environment configuration
JINJA2_ENV = {
    'block_start_string': '\\BLOCK{',
    'block_end_string': '}',
    'variable_start_string': '\\VAR{',
    'variable_end_string': '}',
    'comment_start_string': '\\#{',
    'comment_end_string': '}',
    'trim_blocks': True,
    'autoescape': False
}

class JinjaLatexResume:
    """
    Class to generate LaTeX resumes using a Jinja2 template (provided as a string)
    and convert them to PDF.
    """

    def __init__(self, name, email, phone_num, linkedin_url="", github_url="",
                 work_experience=None, education=None, professional_summary="", skills=None):
        """
        Initialize the resume with dynamic data.
        
        work_experience should be a list of dictionaries with keys such as:
          role, company, start_date, end_date, location, description.
          
        education should be a list of dictionaries with keys such as:
          degree, institution, start_date, end_date, location, description.
          
        professional_summary is a string summarizing your professional profile.
        
        skills should be a list of dictionaries, each with:
          - "category": The skill category (e.g., "Programming Languages")
          - "skills_list": A string listing the skills (e.g., "Python, R, SQL, ...")
        """
        self.name = name
        self.email = email
        self.phone_num = phone_num
        self.linkedin_url = linkedin_url
        self.github_url = github_url
        self.work_experience = work_experience if work_experience is not None else []
        self.education = education if education is not None else []
        self.professional_summary = professional_summary
        self.skills = skills if skills is not None else []

        # Use the imported template content
        self.template_content = tex_template_content

        # Google Drive folder IDs (set these to your actual folder IDs)
        self.latex_folder_id = "YOUR_LATEX_FOLDER_ID"
        self.pdf_folder_id = "YOUR_PDF_FOLDER_ID"
        self.gdrive_handler = GoogleDriveHandler()

        # Output directory for generated PDFs
        self.pdf_output_dir = os.path.join(os.getcwd(), "generated_pdfs")
        os.makedirs(self.pdf_output_dir, exist_ok=True)

        self.rendered_latex = ""  # To store rendered LaTeX content

        # Create a Jinja2 environment using the custom settings.
        self.jinja_env = Environment(**JINJA2_ENV)

    def render_template(self):
        """
        Renders the LaTeX template using the Jinja2 environment and stores it as a string.
        The template uses placeholders like \VAR{name}, \VAR{email}, and blocks for work_experience,
        education, professional_summary, and skills.
        """
        template = self.jinja_env.from_string(self.template_content)
        self.rendered_latex = template.render(
            name=self.name,
            email=self.email,
            phone=self.phone_num,       # Template uses \VAR{phone}
            linkedin=self.linkedin_url,
            github=self.github_url,
            work_experience=self.work_experience,
            education=self.education,
            professional_summary=self.professional_summary,
            skills=self.skills
        )
        return self.rendered_latex

    def save_as_tex(self, filename="resume.tex"):
        """
        Saves the rendered LaTeX content to a .tex file and uploads it to Google Drive.
        """
        self.render_template()  # Ensure the template is rendered

        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.rendered_latex)
        print(f"✅ LaTeX file saved: {filename}")

        uploaded_file_id = self.gdrive_handler.upload_file(filename, filename)
        print(f"✅ LaTeX file uploaded to Google Drive with ID: {uploaded_file_id}")
        return uploaded_file_id

    def save_as_pdf(self, filename="resume.pdf"):
        """
        Generates a PDF from the rendered LaTeX content and uploads it to Google Drive.
        """
        if not self.rendered_latex:
            self.render_template()

        # Use a temporary .tex filename based on the PDF filename.
        latex_filename = filename.replace(".pdf", ".tex")
        final_pdf_path = os.path.join(self.pdf_output_dir, filename)

        # Save the rendered LaTeX to a temporary .tex file.
        with open(latex_filename, "w", encoding="utf-8") as f:
            f.write(self.rendered_latex)
        print(f"✅ Temporary LaTeX file saved: {latex_filename}")

        try:
            # Read the .tex file as binary data.
            with open(latex_filename, "rb") as tex_file:
                tex_content = tex_file.read()

            # Create a PDFLaTeX instance from the binary string.
            pdfl = PDFLaTeX.from_binarystring(tex_content, "resume_output")
            # Force the output directory to our designated folder.
            pdfl.set_output_directory(self.pdf_output_dir)

            # Generate the PDF; keep_pdf_file and keep_log_file are True for debugging.
            pdf_data, log_data, process = pdfl.create_pdf(
                keep_pdf_file=True,
                keep_log_file=True,
                env=os.environ
            )

            # PDFLaTeX names the output PDF as "resume_output.pdf"
            generated_pdf_path = os.path.join(self.pdf_output_dir, "resume_output.pdf")
            if os.path.exists(generated_pdf_path):
                shutil.move(generated_pdf_path, final_pdf_path)
                print(f"✅ PDF successfully generated and saved to: {final_pdf_path}")
            else:
                print("❌ PDF generation failed. Check LaTeX logs for errors.")
                log_file_path = os.path.join(self.pdf_output_dir, "resume_output.log")
                if os.path.exists(log_file_path):
                    with open(log_file_path, "r", encoding="utf-8") as log_file:
                        print("📄 LaTeX Log Output:\n", log_file.read())
                return None

            # Upload the PDF file to Google Drive.
            uploaded_file_id = self.gdrive_handler.upload_file(final_pdf_path, filename)
            print(f"✅ PDF file uploaded to Google Drive with ID: {uploaded_file_id}")
            return uploaded_file_id

        except Exception as e:
            print(f"❌ Error during PDF generation: {e}")
            return None

# --- Usage Example ---
if __name__ == "__main__":
    work_exp = [
        {
            "role": "Senior Data Scientist",
            "company": "Tror - AI for Everyone",
            "start_date": "Dec 2022",
            "end_date": "Present",
            "location": "Nashville, TN",
            "description": r"""
\begin{itemize}
  \item Developed a Generative AI chat agent using Langchain, LangGraph, LlamaIndex, and Haystack, incorporating multi-agent RAG workflows for seamless user-specific interactions.
  \item Integrated multi-agent AI chatbots with RAG-enabled knowledge bases for document support, web search, tool calls, and secure fine-tuned model usage; leveraged MongoDB for chat history storage.
  \item Streamlined workflows with Apache Airflow to process documents and embed data using open-source models.
  \item Built APIs with FastAPI and gRPC microservices; integrated Confluence and GDrive for knowledge bases.
  \item Improved chat performance with Redis Cache, minimizing database queries and reducing costs.
  \item Adopted Agile Scrum practices with Jira for sprint planning and team collaboration.
  \item Utilized APIs (GPT, Claude) and deployed open-source models like LLaMA on AWS SageMaker with Amazon Bedrock integration.
  \item Integrated Stripe for payment processing and implemented voice transcription to enhance accessibility.
  \item Created medical image segmentation models for brain and pancreas tumor detection using PyTorch.
  \item Developed a voice transcription app with 95.6\% accuracy for North American accents using Whisper AI.
  \item Utilized Kafka to build real-time data pipelines for efficient data streaming.
  \item Monitored ML models for drift and performance issues using WhyLabs, Splunk, and Datadog.
  \item Managed the full lifecycle of ML models, including deployment and integration into data pipelines and BI tools.
  \item Enhanced data reliability using Azure Cosmos DB, AKS, Databricks, and MLOps best practices.
  \item Implemented Docker and Kubernetes for containerization and orchestration of AI workflows.
  \item Optimized PyTorch and TensorFlow pipelines on Ubuntu for resource-efficient training and inference.
  \item Streamlined CI/CD pipelines for AI applications with Harness and Jenkins.
\end{itemize}
"""
        },
        {
            "role": "Data Engineer",
            "company": "Client: Kimberly-Clark, Tredence Solutions Private Limited",
            "start_date": "May 2022",
            "end_date": "Dec 2022",
            "location": "Bangalore, India",
            "description": r"""
\begin{itemize}
  \item Developed and managed data pipelines with Azure Data Factory (ADF), Snowflake, and Databricks to optimize data transformations.
  \item Utilized PySpark on Azure Databricks for processing and analyzing large datasets.
  \item Integrated Oracle SQL for advanced querying and data manipulation.
  \item Implemented Apache Airflow for task scheduling, monitoring, and error handling.
  \item Employed Azure DevOps for version control, CI/CD pipelines, and automated deployments.
  \item Used Azure Boards for sprint planning and Agile task tracking.
  \item Applied SDLC practices for scalable data engineering solutions.
\end{itemize}
"""
        },
        {
            "role": "Data Scientist Intern",
            "company": "Tror - AI for Everyone",
            "start_date": "May 2021",
            "end_date": "May 2022",
            "location": "Hyderabad, India",
            "description": r"""
\begin{itemize}
  \item Contributed to a Master Data Management (MDM) backend workflow using Langchain and PyTorch, integrating Redis cache for efficient data retrieval.
  \item Assisted in a lung cancer detection project by implementing preprocessing techniques with OpenCV and TensorFlow, and improving segmentation with transformer-based models.
  \item Developed an ETL pipeline with Apache Airflow to preprocess loan application data and deploy a binary classification ML model.
\end{itemize}
"""
        }
    ]
    
    education = [
        {
            "degree": "Masters in Information Technology Management",
            "institution": "Webster University",
            "start_date": "Sep 2023",
            "end_date": "Dec 2024",
            "location": "San Antonio, TX",
            "description": "GPA: 3.93/4.0"
        },
        {
            "degree": "Bachelor of Technology in Mechanical Engineering",
            "institution": "National Institute of Technology, Surat (SVNIT)",
            "start_date": "Jul 2018",
            "end_date": "May 2022",
            "location": "Surat, India",
            "description": "GPA: 8.02/10.0"
        }
    ]
    
    professional_summary = (
        "Dynamic and results-driven Data Scientist and Generative AI expert with more than three years of professional experience in designing, deploying, and optimizing AI and data-driven solutions. Proficient in developing scalable machine learning pipelines, fine-tuning large language models, and implementing full-stack web applications. Skilled in leveraging cloud platforms, containerization, and modern frameworks (PyTorch, TensorFlow, LangChain). Adept at collaborating with cross-functional teams to deliver innovative solutions that enhance operational efficiency and drive business growth."
    )
    
    skills = [
        {
            "category": "Programming Languages",
            "skills_list": "Python, R, SQL, Java, PySpark, Linux"
        },
        {
            "category": "Cloud Platforms and DevOps",
            "skills_list": "AWS, Azure, Docker, Kubernetes, Datadog, Amazon Bedrock, Git, GitHub, SSH, Harness, Jenkins, Snowflake, Apache Airflow, ADF, AWS SageMaker, Databricks, Oracle SQL, MongoDB Atlas, PostgreSQL, SQL Server, Kafka, Pandas, PowerBI"
        },
        {
            "category": "Machine Learning",
            "skills_list": "PyTorch, TensorFlow, Scikit-learn, Regression, Hypothesis Testing, Feature Engineering, Model Deployment, Workflow Automation, Model Monitoring, Model Drift Detection, Data Drift Detection"
        },
        {
            "category": "Generative AI",
            "skills_list": "OpenCV, Deep Learning, NLP, Fine-tuning LLMs, Medical Imaging (Segmentation and Classification), Generative AI, RAG Implementation, Re-ranking, Hugging Face, Vector Databases, Embedding Models, Prompting Techniques, Whisper AI, Azure AI Studio, Langchain, LangGraph, LlamaIndex, Haystack, Vertex AI"
        },
        {
            "category": "Software Frameworks and Tools",
            "skills_list": "Flask, FastAPI, SciPy, Redis, gRPC, NumPy, Pandas, Agile (Scrum), CI/CD, MLOps/LLMOps (Airflow, Mlflow), Data Orchestration, WhyLabs, Splunk, Azure Cosmos DB, PowerBI"
        }
    ]
    
    resume = JinjaLatexResume(
        name="Kushwanth Kumar Karamsetti",
        email="kkushwanth77@gmail.com",
        phone_num="+1 (929) 361-8554",
        linkedin_url="kushwanthkaramsetti",
        github_url="kushwanth2210",
        work_experience=work_exp,
        education=education,
        professional_summary=professional_summary,
        skills=skills
    )
    
    resume.render_template()       # Render the template and preview (optional)
    resume.save_as_tex("my_resume.tex")
    resume.save_as_pdf("my_resume.pdf")
