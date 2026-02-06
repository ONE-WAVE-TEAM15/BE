from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None
    skills_used: Optional[str] = None
    results: Optional[str] = None
    is_public: bool = True
    display_order: Optional[int] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None
    skills_used: Optional[str] = None
    results: Optional[str] = None
    is_public: Optional[bool] = None
    display_order: Optional[int] = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None
    skills_used: Optional[str] = None
    results: Optional[str] = None
    is_public: bool
    display_order: Optional[int] = None

    class Config:
        from_attributes = True
