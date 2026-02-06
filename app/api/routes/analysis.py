from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models import User, Project, Job
from app.schemas.analysis import PortfolioAnalysisResponse
from app.utils.ai_analysis import analyze_portfolio

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/portfolio", response_model=PortfolioAnalysisResponse)
async def analyze_user_portfolio(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Analyze user's portfolio fit against job openings.

    Automatically selects:
    - User's most recent project
    - First job matching user's domain

    Returns AI-generated analysis with skill match, fit score,
    missing competencies, and recommended training programs.
    """
    # Validate user has domain
    if not current_user.domain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="사용자의 도메인이 설정되지 않았습니다. 먼저 설문조사를 완료해주세요."
        )

    # Fetch most recent project
    project_statement = (
        select(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
        .limit(1)
    )
    project = session.exec(project_statement).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="분석할 프로젝트가 없습니다. 먼저 프로젝트를 등록해주세요."
        )

    # Fetch job matching user's domain
    job_statement = (
        select(Job)
        .where(Job.domain == current_user.domain)
        .limit(1)
    )
    job = session.exec(job_statement).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{current_user.domain} 도메인에 매칭되는 채용공고를 찾을 수 없습니다."
        )

    # Build data dictionaries for analyze_portfolio
    user_data = {
        "self_summary": current_user.self_summary or "",
        "survey_text": current_user.survey_text or "",
        "skills": current_user.skills or ""
    }

    project_data = {
        "title": project.title,
        "content": project.content or "",
        "skills_used": project.skills_used or ""
    }

    job_data = {
        "company": job.company,
        "title": job.title,
        "description": job.description,
        "skills_required": job.skills_required or ""
    }

    # Call AI analysis
    try:
        analysis_result = analyze_portfolio(user_data, project_data, job_data)

        # Check if result contains error
        if isinstance(analysis_result, dict) and "error" in analysis_result:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI 분석 오류: {analysis_result['error']}"
            )

        # Add metadata for tracking
        analysis_result["analyzed_project"] = project.title
        analysis_result["analyzed_job"] = f"{job.company} - {job.title}"

        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"포트폴리오 분석 중 오류가 발생했습니다: {str(e)}"
        )
