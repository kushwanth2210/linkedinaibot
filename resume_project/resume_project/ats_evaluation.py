import re
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

# Ensure the necessary NLTK data is downloaded
nltk.download('stopwords')

class ATSAnalyzer:
    def __init__(self, job_description, resume_text):
        """
        Initialize ATS Analyzer with job description and resume text (both as strings).
        """
        self.job_description = job_description
        self.resume_text = resume_text
        self.stop_words = set(stopwords.words("english"))

    def extract_text_from_latex(self, latex_content):
        """
        Extract plain text from LaTeX content by removing LaTeX commands.
        """
        # Remove LaTeX commands
        text = re.sub(r'\\[a-zA-Z]+', '', latex_content)
        # Remove curly braces
        text = re.sub(r'{|}', '', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
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
        Preprocesses both resume and job description, and calculates ATS score.
        """
        # Extract plain text from LaTeX resume content
        plain_resume_text = self.extract_text_from_latex(self.resume_text)
        
        if not plain_resume_text:
            print("Error: Could not extract text from the resume content.")
            return None
        
        # Preprocess text
        job_description_text = self.preprocess_text(self.job_description)
        resume_text = self.preprocess_text(plain_resume_text)

        # Compute similarity score
        ats_score = self.compute_similarity(job_description_text, resume_text)
        return ats_score

# Example usage
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

# Sample LaTeX-formatted resume content
resume_text = r"""
\documentclass{resume}
\begin{document}
\name{John Doe}
\contact{john.doe@example.com}{(123) 456-7890}
\section{Experience}
\begin{entry}
\title{Software Engineer}{Tech Company}
\location{San Francisco, CA}
\dates{Jan 2020 -- Present}
\body{
\begin{itemize}
\item Developed machine learning models using Python libraries such as NumPy and TensorFlow.
\item Implemented research papers into production-level code.
\item Contributed to open-source AI/ML projects.
\item Collaborated with cross-functional teams to deploy AI solutions.
\end{itemize}
}
\end{entry}
\end{document}
"""

ats_analyzer = ATSAnalyzer(job_description, resume_text)
score = ats_analyzer.get_ats_score()

if score is not None:
    print(f"ATS Match Score: {score}%")
    if score >= 75:
        print("✅ Resume is well-matched to the job. Good to apply!")
    elif 50 <= score < 75:
        print("⚠️ Resume is somewhat relevant, but improvements are recommended.")
    else:
        print("❌ Resume is a poor match. Consider tailoring it to the job description.")
