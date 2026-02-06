from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone_number: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SurveyCreate(BaseModel):
    domain: str
    text: str


class PortfolioCreate(BaseModel):
    self_summary: Optional[str] = None
    user_skills: Optional[str] = None
    external_links: Optional[str] = None

    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None
    skills_used: Optional[str] = None
    results: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone_number: Optional[str] = None
    domain: Optional[str] = None
    survey_text: Optional[str] = None
    self_summary: Optional[str] = None
    skills: Optional[str] = None
    external_links: Optional[str] = None

    class Config:
        from_attributes = True
