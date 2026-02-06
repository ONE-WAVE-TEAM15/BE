from pydantic import BaseModel, Field
from typing import Optional, List


class ConversationMessage(BaseModel):
    """A single message in the conversation history"""
    role: str  # "interviewer", "user", "mentor"
    content: str


class ProjectInfo(BaseModel):
    """Project information returned from /interview/start"""
    id: int
    title: str
    skills_used: str


class InterviewStartResponse(BaseModel):
    """Response for POST /interview/start"""
    message: str
    audio: str
    project: ProjectInfo


class InterviewerChatRequest(BaseModel):
    """Request for POST /interview/chat/interviewer"""
    user_answer: str = Field(..., min_length=1, max_length=2000)
    conversation_history: Optional[List[ConversationMessage]] = []


class InterviewerChatResponse(BaseModel):
    """Response for POST /interview/chat/interviewer"""
    message: str
    audio: str


class MentorChatRequest(BaseModel):
    """Request for POST /interview/chat/mentor"""
    interviewer_question: str = Field(..., min_length=1)
    user_answer: str = Field(..., min_length=1, max_length=2000)
    conversation_history: Optional[List[ConversationMessage]] = []


class MentorChatResponse(BaseModel):
    """Response for POST /interview/chat/mentor"""
    feedback: str
    tips: List[str]
