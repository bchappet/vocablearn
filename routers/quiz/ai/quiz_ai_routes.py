
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.database import SessionDep
from models.tables import Word, Group
from .. import session_manager

router = APIRouter(
    prefix="/quiz/ai",
    tags=["quiz/ai"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/{session_id}", name='quiz_ai', response_class=HTMLResponse)
async def quiz_ai(request: Request, session_id: str):
    """user click on ai option in quiz answer screen"""
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    question_id = quiz_session['question_id']
    focus_word = quiz_session['words'][question_id]
    return templates.TemplateResponse(
        "ai/quiz_ai.html",
        {
            "request": request,
            "focus_word_primary": focus_word.primary_text,
            "focus_word_secondary": focus_word.secondary_text,
        }
    )


@router.get("/mnemonic/{word}", name='generate_mnemonic')
async def generate_mnemonic(request: Request, word: str):
    return {'word': word}