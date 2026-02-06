from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models import User
from app.schemas import SurveyCreate

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
