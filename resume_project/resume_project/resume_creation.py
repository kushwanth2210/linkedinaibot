import os
import shutil
from jinja2 import Environment
from pdflatex import PDFLaTeX
from storage.gdrive import GoogleDriveHandler  # Ensure your GoogleDriveHandler is correctly imported
from resume_templates.latex_templates import tex_template_content

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

    def __init__(self, name, email, phone_num, linkedin_url="", github_url="", work_experience=None):
        """
        Initialize the resume with dynamic data.
        work_experience should be a list of dictionaries with keys such as:
          role, company, start_date, end_date, location, description.
        """
        self.name = name
        self.email = email
        self.phone_num = phone_num
        self.linkedin_url = linkedin_url
        self.github_url = github_url
        self.work_experience = work_experience if work_experience is not None else []

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
        The template uses placeholders like \VAR{name}, \VAR{email}, and a block for work_experience.
        """
        template = self.jinja_env.from_string(self.template_content)
        self.rendered_latex = template.render(
            name=self.name,
            email=self.email,
            phone=self.phone_num,       # Template uses \VAR{phone}
            linkedin=self.linkedin_url,
            github=self.github_url,
            work_experience=self.work_experience
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
            "role": "Software Engineer",
            "company": "Tech Solutions Inc.",
            "start_date": "Jan 2019",
            "end_date": "Present",
            "location": "Example City",
            "description": "Developed and maintained web applications using Python and JavaScript. Collaborated with cross-functional teams."
        },
        {
            "role": "Intern",
            "company": "Startup XYZ",
            "start_date": "Jun 2018",
            "end_date": "Dec 2018",
            "location": "Example City",
            "description": "Assisted in the development of mobile applications and performed testing."
        }
    ]
    
    resume = JinjaLatexResume(
        name="John Doe",
        email="johndoe@example.com",
        phone_num="929-361-8554",
        linkedin_url="johndoe",
        github_url="johndoe",
        work_experience=work_exp
    )
    resume.render_template()       # Render the template and preview (optional)
    resume.save_as_tex("my_resume.tex")
    resume.save_as_pdf("my_resume.pdf")
