from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Signup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    activity_id: int = Field(foreign_key="activity.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relationships
    user: "User" = Relationship(back_populates="signups")
    activity: "Activity" = Relationship(back_populates="signups")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    signups: List[Signup] = Relationship(back_populates="user")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: int = 0
    signups: List[Signup] = Relationship(back_populates="activity")

