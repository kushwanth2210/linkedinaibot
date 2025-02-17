import pdfplumber
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

nltk.download('stopwords')

class ATSAnalyzer:
    def __init__(self, job_description, resume_path):
        """
        Initialize ATS Analyzer with job description (as a string) and resume PDF path.
        """
        self.job_description = job_description
        self.resume_path = resume_path
        self.stop_words = set(stopwords.words("english"))

    def extract_text_from_pdf(self, file_path):
        """
        Extract text from a given PDF file.
        """
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n" if page.extract_text() else ""
        return text.strip()

    def preprocess_text(self, text):
        """
        Preprocess text: convert to lowercase, remove punctuation, and remove stopwords.
        """
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))  
        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        return " ".join(words)

    def compute_similarity(self, text1, text2):
        """
        Compute TF-IDF vectorization and cosine similarity between two texts.
        """
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return round(similarity_score * 100, 2)

    def get_ats_score(self):
        """
        Extracts resume text, preprocesses both resume and job description, and calculates ATS score.
        """
        resume_text = self.extract_text_from_pdf(self.resume_path)
        
        if not resume_text:
            print("Error: Could not extract text from the resume file.")
            return None
        
        # Preprocess text
        job_description_text = self.preprocess_text(self.job_description)
        resume_text = self.preprocess_text(resume_text)

        # Compute similarity score
        ats_score = self.compute_similarity(job_description_text, resume_text)
        return ats_score


job_description = """
Netflix is looking for a Software Engineer (L5), Python Platform. The candidate must have expertise in:
- Python (NumPy, TensorFlow, PyTorch, Scikit-learn)
- Research paper implementation
- Generative AI (GANs, VAEs, transformers)
- Open-source contributions in AI/ML
- NLP and data processing (feature engineering, model evaluation)
- AI/ML security (risk management, robustness testing, cloud deployment with CI/CD, API design)
- Strong collaboration and cross-functional teamwork.

The candidate should demonstrate experience in:
- End-to-end model deployment and scaling
- Researching and implementing algorithms
- Working on large-scale distributed systems
"""

resume_file = "updated_resume.pdf"

ats_analyzer = ATSAnalyzer(job_description, resume_file)
score = ats_analyzer.get_ats_score()

if score is not None:
    print(f"ATS Match Score: {score}%")
    if score >= 75:
        print("✅ Resume is well-matched to the job. Good to apply!")
    elif 50 <= score < 75:
        print("⚠️ Resume is somewhat relevant, but improvements are recommended.")
    else:
        print("❌ Resume is a poor match. Consider tailoring it to the job description.")
