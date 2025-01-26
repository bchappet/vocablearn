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
    english: str = Field(index=True)
    russian: str = Field(index=True)
    group_id: int = Field(foreign_key="group.id")
    mnemonic: str | None = None
    mastery: float = Field(default=0.0)
    success_count: int = Field(default=0)
    attempt_count: int = Field(default=0)
    
    group: Group = Relationship(back_populates="words")
    progress: List["WordProgress"] = Relationship(back_populates="word")

class WordProgress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    word_id: int = Field(foreign_key="word.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ru_to_en: bool
    correct: bool
    response_time: float  # in seconds
    
    word: Word = Relationship(back_populates="progress")

class Settings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ru_to_en: bool = Field(default=False)
    nb_questions: int = Field(default=5)
