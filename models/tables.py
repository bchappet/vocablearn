from typing import List
from sqlmodel import Field, SQLModel, Relationship

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
    
    group: Group = Relationship(back_populates="words")

class Settings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ru_to_en: bool = Field(default=False)
    nb_questions: int
