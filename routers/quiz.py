from typing import Dict, List, Tuple
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.database import SessionDep
from sqlalchemy import func
from models.tables import Word, Settings
from utils.web import is_mobile
from utils.web import is_mobile, russian_keyboard_layout
import uuid

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"]
)

templates = Jinja2Templates(directory="templates")

# In-memory session storage (replace with database in production)
sessions: Dict[str, dict] = {}

def choose_next_words(db: SessionDep, nb_words_to_choose: int) -> List[dict]:
    """
    Returns a list of random words from the database.
    Each word is a dictionary containing 'english' and 'russian' translations.
    """
    words = db.query(Word).order_by(func.random()).limit(nb_words_to_choose).all()
    settings = db.query(Settings).first()
    if settings.ru_to_en:
        return [{"question": word.russian, "answer": word.english} for word in words]
    else:
        return [{"question": word.english, "answer": word.russian} for word in words]

@router.get("/", name="read_quiz", response_class=HTMLResponse)
def read_quiz(request: Request, db: SessionDep):
    nb_words_available = db.query(Word).count()
    settings = db.query(Settings).first()
    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context={
            "nb_words_available": nb_words_available,
            "settings": settings
        }
    )

@router.post("/session", name="create_quiz_session")
async def create_quiz_session(db: SessionDep):
    settings = db.query(Settings).first()
    session_id = str(uuid.uuid4())
    if not settings:
        return RedirectResponse("/manage/", status_code=303)
    words = choose_next_words(db, settings.nb_questions)
    quiz_session = {
        "session_id": session_id,
        "question_id": 0,
        "words": words,
        "answers": [],
        "score": 0,
    }
    sessions[session_id] = quiz_session
    
    # Redirect to first question
    return RedirectResponse(f"/quiz/{session_id}/question", status_code=303)


@router.get("/{session_id}/question", name="quiz_question", response_class=HTMLResponse)
def quiz_question(request: Request, session_id: str, db: SessionDep):
    quiz_session = sessions.get(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    nb_questions = len(quiz_session["words"])
    question_id = quiz_session["question_id"]
    if question_id >= nb_questions:
        return RedirectResponse(f"/quiz/{session_id}/summary", status_code=303)
    
    word = quiz_session["words"][question_id]
    russian_layout = russian_keyboard_layout()
    user_agent = request.headers.get("user-agent", "")
    is_mobile_device = is_mobile(user_agent)
    
    settings = db.query(Settings).first()
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_question.html",
        context={"word_to_translate": word["question"],
                 "question_id": question_id,
                 "nb_questions": nb_questions,
                 "russian_layout": russian_layout,
                 "is_mobile_device": is_mobile_device,
                 "ru_to_en": settings.ru_to_en}
    )

@router.post("/{session_id}/answer", name="quiz_answer")
async def submit_answer(session_id: str, request: Request):
    quiz_session = sessions.get(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    form = await request.form()
    user_answer = form.get("answer")
    
    question_id = quiz_session["question_id"]
    word = quiz_session["words"][question_id]
    correct_answer = word["answer"]
    
    if user_answer == correct_answer:
        quiz_session["score"] += 1
    
    quiz_session["question_id"] += 1
    quiz_session["answers"].append(user_answer)
    return RedirectResponse(f"/quiz/{session_id}/answer", status_code=303)

@router.get("/{session_id}/answer", name="quiz_answer", response_class=HTMLResponse)
def quiz_answer(request: Request, session_id: str):
    quiz_session = sessions.get(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    previous_question = quiz_session["question_id"] - 1
    word = quiz_session["words"][previous_question]
    correct_answer = word["answer"]
    last_answer = quiz_session["answers"][previous_question]
    is_correct = last_answer == correct_answer
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_answer.html",
        context={
            "word": word["question"],
            "user_answer": last_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        }
    )

@router.get("/{session_id}/summary", name="quiz_summary", response_class=HTMLResponse)
def quiz_summary(request: Request, session_id: str):
    quiz_session = sessions.get(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_summary.html",
        context={
            "score": quiz_session["score"],
            "nb_questions": len(quiz_session["words"])
        }
    )


