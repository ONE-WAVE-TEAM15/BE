from pydantic import BaseModel
from typing import List, Optional

class RecommendedProgram(BaseModel):
    """Training program recommended by AI"""
    program_name: str
    domain: str
    start_date: str
    due_date: str
    program_skills: str
    program_content: str
    program_link: str
    program_category: str
    recommendation_reason: str  # Added by AI

class PortfolioAnalysisResponse(BaseModel):
    """Response for POST /analysis/portfolio"""
    skill_match: str
    fit_evaluation: str
    missing_competencies: List[str]
    overall_score: int
    recommended_programs: List[RecommendedProgram]
    analyzed_project: Optional[str] = None
    analyzed_job: Optional[str] = None
