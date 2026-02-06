from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.job import Job
from app.schemas.job import JobsResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=JobsResponse)
def get_jobs(
    domain: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(Job)
    if domain:
        query = query.where(Job.domain == domain)

    jobs = session.exec(query).all()
    return {"jobs": jobs}
