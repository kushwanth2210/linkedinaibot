"""
Resume Project - Package Initialization

This package provides modules for:
- Resume updating with AI assistance
- ATS evaluation for job applications
- LinkedIn job scraping for relevant opportunities
"""

__version__ = "0.1.0"

# from .ats_evaluation import ATSAnalyzer
from .resume_creation import JinjaLatexResume
from .linkedin_agent import LinkedInJobScraper

__all__ = [
    # "ATSAnalyzer",
    "JinjaLatexResume",
    "LinkedInJobScraper",
]
