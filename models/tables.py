from typing import List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    
    words: List["Word"] = Relationship(back_populates="group")

class Word(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    primary_text: str = Field(index=True)  # For now it is english
    secondary_text: str = Field(index=True)  # For now it is russian
    group_id: int = Field(foreign_key="group.id")
    mnemonic: str | None = None
    mastery: float = Field(default=0.0)
    success_count: int = Field(default=0)
    attempt_count: int = Field(default=0)
    
    group: Group = Relationship(back_populates="words")

    def __repr__(self) -> str:
        return f"{self.primary_text}"
