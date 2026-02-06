from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.project import Project


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    name: str
    phone_number: Optional[str] = None
    domain: Optional[str] = None

    # Profile information
    survey_text: Optional[str] = None
    self_summary: Optional[str] = None
    skills: Optional[str] = None
    external_links: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    projects: List["Project"] = Relationship(back_populates="user")
