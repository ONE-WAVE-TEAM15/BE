from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models import Project, User
from app.schemas.interview import (
    InterviewerChatRequest,
    InterviewerChatResponse,
    InterviewStartResponse,
    MentorChatRequest,
    MentorChatResponse,
    ProjectInfo,
)
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Start a new mock interview session.

    Logic:
    1. Fetch user's most recent project
    2. Generate Korean greeting
    3. Convert greeting to audio (TTS)
    4. Return greeting text + base64 audio + project info

    Returns:
        InterviewStartResponse with greeting message, audio, and project info

    Raises:
        HTTPException 400: If user has no projects
        HTTPException 502: If TTS service fails
    """
    # 1. Fetch most recent project
    statement = (
        select(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
        .limit(1)
    )
    project = session.exec(statement).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="사용자에게 프로젝트가 없습니다. 먼저 프로젝트를 생성해주세요."
        )

    # 2. Generate greeting
    llm_service = LLMService()
    greeting = llm_service.format_greeting(
        user_name=current_user.name,
        domain=current_user.domain or "개발",
        project_title=project.title
    )

    # 3. Convert to audio
    try:
        tts_service = TTSService()
        audio_base64 = await tts_service.text_to_speech(greeting)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"TTS 서비스 오류: {str(e)}"
        )

    # 4. Return response
    return InterviewStartResponse(
        message=greeting,
        audio=f"data:audio/mp3;base64,{audio_base64}",
        project=ProjectInfo(
            id=project.id,
            title=project.title,
            skills_used=project.skills_used or ""
        )
    )


@router.post("/chat/interviewer", response_model=InterviewerChatResponse)
async def interviewer_chat(
    request: InterviewerChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Generate interviewer's follow-up question.

    Logic:
    1. Fetch user's most recent project (for tech stack context)
    2. Use Gemini Flash to generate aggressive follow-up question
    3. Convert question to audio (TTS)
    4. Return question text + base64 audio

    Args:
        request: Contains user_answer and optional conversation_history

    Returns:
        InterviewerChatResponse with question message and audio

    Raises:
        HTTPException 400: If user has no projects
        HTTPException 502: If LLM or TTS service fails
    """
    # 1. Fetch most recent project for context
    statement = (
        select(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
        .limit(1)
    )
    project = session.exec(statement).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="프로젝트를 찾을 수 없습니다."
        )

    # 2. Build project context
    project_context = {
        "title": project.title,
        "content": project.content or "",
        "skills_used": project.skills_used or "",
        "results": project.results or ""
    }

    # 3. Generate follow-up question
    llm_service = LLMService()
    try:
        # Convert conversation history to dict format
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in (request.conversation_history or [])
        ]

        question = await llm_service.generate_interviewer_question(
            user_answer=request.user_answer,
            project_context=project_context,
            history=history
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM 서비스 오류: {str(e)}"
        )

    # 4. Convert to audio
    try:
        tts_service = TTSService()
        audio_base64 = await tts_service.text_to_speech(question)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"TTS 서비스 오류: {str(e)}"
        )

    return InterviewerChatResponse(
        message=question,
        audio=f"data:audio/mp3;base64,{audio_base64}"
    )


@router.post("/chat/mentor", response_model=MentorChatResponse)
async def mentor_chat(
    request: MentorChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Generate mentor's constructive feedback.

    Logic:
    1. Use Gemini Pro to analyze interviewer's question and user's answer
    2. Generate constructive feedback in Korean
    3. Provide actionable tips
    4. Return text only (no audio)

    Args:
        request: Contains interviewer_question, user_answer, and optional history

    Returns:
        MentorChatResponse with feedback and tips

    Raises:
        HTTPException 502: If LLM service fails
    """
    # 1. Generate mentor feedback
    llm_service = LLMService()
    try:
        # Convert conversation history to dict format
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in (request.conversation_history or [])
        ]

        feedback_data = await llm_service.generate_mentor_feedback(
            interviewer_question=request.interviewer_question,
            user_answer=request.user_answer,
            history=history
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM 서비스 오류: {str(e)}"
        )

    return MentorChatResponse(
        feedback=feedback_data["feedback"],
        tips=feedback_data["tips"]
    )
