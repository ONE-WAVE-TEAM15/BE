from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    username: str
    domain: Optional[str] = None
    survey_text: Optional[str] = None
    portfolio_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
