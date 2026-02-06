from datetime import date, datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None
    skills_used: Optional[str] = None
    results: Optional[str] = None

    # Additional fields
    is_public: bool = Field(default=True)
    display_order: Optional[int] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Optional["User"] = Relationship(back_populates="projects")
