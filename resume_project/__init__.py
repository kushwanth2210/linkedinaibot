"""
Resume Project - Package Initialization

This package provides modules for:
- Resume updating with AI assistance
- ATS evaluation for job applications
- LinkedIn job scraping for relevant opportunities
"""

__version__ = "0.1.0"

from .update_resume import ResumeUpdater
from .ats_evaluation import ATSAnalyzer
from .resume_creation import ResumeGenerator
from .linkedin_agent import LinkedInJobScraper

__all__ = [
    "ResumeUpdater",
    "ATSAnalyzer",
    "ResumeGenerator",
    "LinkedInJobScraper",
]
