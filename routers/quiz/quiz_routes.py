from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.database import SessionDep
from models.tables import Word, Settings
from utils.web import is_mobile, russian_keyboard_layout
from . import session_manager, word_selector, answer_handler

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"]
)

templates = Jinja2Templates(directory="templates")

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
    if not settings:
        return RedirectResponse("/manage/", status_code=303)
    
    words = word_selector.choose_next_words(db, settings.nb_questions)
    session_id = session_manager.create_session(words)
    return RedirectResponse(f"/quiz/{session_id}/question", status_code=303)

@router.get("/{session_id}/question", name="quiz_question", response_class=HTMLResponse)
def quiz_question(request: Request, session_id: str, db: SessionDep):
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
        
    nb_questions = len(quiz_session["words"])
    question_id = quiz_session["question_id"]
    if question_id >= nb_questions:
        return RedirectResponse(f"/quiz/{session_id}/summary", status_code=303)
    
    word = quiz_session["words"][question_id]
    settings = db.query(Settings).first()
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_question.html",
        context={
            "word_to_translate": word["question"],
            "question_id": question_id,
            "nb_questions": nb_questions,
            "russian_layout": russian_keyboard_layout(),
            "is_mobile_device": is_mobile(request.headers.get("user-agent", "")),
            "ru_to_en": settings.ru_to_en
        }
    )

@router.post("/{session_id}/answer", name="quiz_answer")
async def submit_answer(session_id: str, request: Request, db: SessionDep):
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    form = await request.form()
    user_answer = form.get("answer")
    settings = db.query(Settings).first()
    
    question_id = quiz_session["question_id"]
    word = quiz_session["words"][question_id]
    
    is_correct = answer_handler.process_answer(
        db, word, user_answer, quiz_session["start_time"], settings.ru_to_en
    )
    
    session_manager.update_session_answer(session_id, is_correct, user_answer)
    return RedirectResponse(f"/quiz/{session_id}/answer", status_code=303)

@router.get("/{session_id}/answer", name="quiz_answer", response_class=HTMLResponse)
def quiz_answer(request: Request, session_id: str, db: SessionDep):
    """
    This function is called when the user submits an answer to a quiz question.
    It displays the user's answer and the correct answer for the previous question.
    """
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    previous_question = quiz_session["question_id"] - 1
    last_word = quiz_session["words"][previous_question]
    last_answer = quiz_session["answers"][previous_question]
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_answer.html",
        context={
            "word": last_word["question"],
            "user_answer": last_answer,
            "correct_answer": last_word["answer"],
            "is_correct": last_answer == last_word["answer"],
            "success_count": last_word.success_count,
            "attempt_count": last_word.attempt_count,
        }
    )

@router.get("/{session_id}/summary", name="quiz_summary", response_class=HTMLResponse)
def quiz_summary(request: Request, session_id: str):
    quiz_session = session_manager.get_session(session_id)
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
