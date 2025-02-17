from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from models.tables import Group, Word
from models.database import SessionDep
from sqlmodel import select, func

class WordEntry(BaseModel):
    english: str
    russian: str
    mnemonic: Optional[str] = None

class WordGroupUpdate(BaseModel):
    word_id: int
    new_group_id: int

class WordDelete(BaseModel):
    word_id: int

router = APIRouter(
    prefix="/manage",
    tags=["group-management"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def read_manage(request: Request, session: SessionDep):
    # Query to get all groups with their words
    statement = select(Group)
    groups = session.exec(statement).all()

    # Query to get all groups with word counts
    statement = (
        select(
            Group,
            func.count(Word.id).label("word_count")
        )
        .outerjoin(Word)
        .group_by(Group.id)
    )
    results = session.exec(statement).all()
    # Create list of groups with their word counts
    groups_with_counts = [
        {"name": group.name, "word_count": count}
        for group, count in results
    ]
    print(groups_with_counts)

    return templates.TemplateResponse(
        request=request,
        name="word_management/manage.html",
        context={"groups": groups_with_counts}
    )

@router.get("/add_group", response_class=HTMLResponse)
def read_manage_add_group(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="word_management/manage_add_group.html",
    )

@router.post("/add_group")
async def create_group(request: Request, session: SessionDep):
    form_data = await request.form()
    
    group_name = form_data.get('group_name')
    english_words = form_data.getlist('english[]')
    russian_words = form_data.getlist('russian[]')
    mnemonics = form_data.getlist('mnemonic[]')
    
    # Create the group first
    db_group = Group(name=group_name)
    session.add(db_group)
    session.flush()  # This gets us the group.id
    
    # Create and add words
    for eng, rus, mnem in zip(english_words, russian_words, mnemonics):
        if eng and rus:
            word = Word(
                english=eng,
                russian=rus,
                mnemonic=mnem if mnem else "",
                group_id=db_group.id
            )
            session.add(word)
    
    # Update group statistics
    db_group.total_words = len([w for w in zip(english_words, russian_words) if w[0] and w[1]])
    db_group.average_mastery = 0.0  # Initial mastery
    
    session.commit()
    return RedirectResponse(url="/manage", status_code=303)

@router.get("/word_details", response_class=HTMLResponse)
def read_word_details(request: Request, session: SessionDep):
    # Query to get all words with their group names
    statement = (
        select(
            Word,
            Group.name.label("group_name")
        )
        .join(Group)
        .order_by(Group.name, Word.primary_text)
    )
    results = session.exec(statement).all()
    
    # Query to get all groups for the filter
    groups = session.exec(select(Group)).all()
    
    # Prepare word data
    words_data = [
        {
            "group_id": str(word.group_id),
            "group_name": group_name,
            "primary_text": word.primary_text,
            "secondary_text": word.secondary_text,
            "mnemonic": word.mnemonic,
            "mastery": word.mastery,
            "attempt_count": word.attempt_count
        }
        for word, group_name in results
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="word_management/word_details.html",
        context={
            "words": words_data,
            "groups": groups
        }
    )

@router.get("/manage_group", response_class=HTMLResponse)
def read_manage_group(request: Request, session: SessionDep):
    # Query to get all groups with their words
    statement = (
        select(
            Group,
            func.count(Word.id).label("word_count")
        )
        .outerjoin(Word)
        .group_by(Group.id)
    )
    results = session.exec(statement).all()
    
    # Get words for each group
    groups_with_data = []
    for group, count in results:
        words = session.exec(
            select(Word).where(Word.group_id == group.id)
        ).all()
        groups_with_data.append({
            "id": group.id,
            "name": group.name,
            "word_count": count,
            "words": words
        })

    return templates.TemplateResponse(
        request=request,
        name="word_management/manage_group.html",
        context={"groups": groups_with_data}
    )

@router.post("/update_word_group")
async def update_word_group(data: WordGroupUpdate, session: SessionDep):
    word = session.get(Word, data.word_id)
    if word:
        word.group_id = data.new_group_id
        session.add(word)
        session.commit()
        return {"status": "success"}
    return {"status": "error", "message": "Word not found"}

@router.post("/delete_word")
async def delete_word(data: WordDelete, session: SessionDep):
    word = session.get(Word, data.word_id)
    if word:
        session.delete(word)
        session.commit()
        return {"status": "success"}
    return {"status": "error", "message": "Word not found"}
