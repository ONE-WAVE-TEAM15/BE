from typing import Optional

from pydantic import BaseModel


class JobCreate(BaseModel):
    company: str
    title: str
    description: str
    domain: Optional[str] = None
    skills_required: Optional[str] = None


class JobUpdate(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    skills_required: Optional[str] = None


class JobResponse(BaseModel):
    id: int
    company: str
    title: str
    description: str
    domain: Optional[str] = None
    skills_required: Optional[str] = None

    class Config:
        from_attributes = True


class JobsResponse(BaseModel):
    jobs: list[JobResponse]
