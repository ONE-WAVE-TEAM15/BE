from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models import Project, User
from app.schemas import PortfolioCreate, SurveyCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/me/survey")
def update_survey(
    survey_in: SurveyCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    current_user.domain = survey_in.domain
    current_user.survey_text = survey_in.text
    session.add(current_user)
    session.commit()
    return {"msg": "Survey updated"}


@router.post("/me/portfolio")
def create_portfolio(
    portfolio_in: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # Update User Profile
    if portfolio_in.self_summary is not None:
        current_user.self_summary = portfolio_in.self_summary
    if portfolio_in.user_skills is not None:
        current_user.skills = portfolio_in.user_skills
    if portfolio_in.external_links is not None:
        current_user.external_links = portfolio_in.external_links

    session.add(current_user)

    # Create Project
    project = Project(
        title=portfolio_in.title,
        start_date=portfolio_in.start_date,
        end_date=portfolio_in.end_date,
        content=portfolio_in.content,
        skills_used=portfolio_in.skills_used,
        results=portfolio_in.results,
        user_id=current_user.id,
    )
    session.add(project)

    session.commit()
    session.refresh(project)

    return {"msg": "Portfolio created successfully", "project_id": project.id}
