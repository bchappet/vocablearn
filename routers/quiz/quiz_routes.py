from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.database import SessionDep
from models.tables import Word, Group
from utils.web import is_mobile, russian_keyboard_layout
from . import session_manager, word_selector, answer_handler
from sqlalchemy import func

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", name="read_quiz", response_class=HTMLResponse)
def read_quiz(request: Request, db: SessionDep):
    nb_words_available = db.query(Word).count()
    return templates.TemplateResponse(
        request=request,
        name="quiz_menu.html",
        context={
            "nb_words_available": nb_words_available,
        }
    )

@router.get("/focus", name="quiz_focus", response_class=HTMLResponse)
def quiz_focus(request: Request, db: SessionDep):
    # Get all distinct groups with their word counts and details
    groups = db.query(
        Word.group_id,
        Group.name,
        Group.description,
        func.count(Word.id).label('word_count')
    ).join(Group, Word.group_id == Group.id)\
    .group_by(Word.group_id, Group.name, Group.description).all()
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_focus.html",
        context={
            "groups": groups
        }
    )

@router.post("/session")
async def create_quiz_session(
    request: Request,
    db: SessionDep
):
    form = await request.form()
    nb_questions = int(form.get("nb_questions", 10))
    primary_to_secondary = form.get("direction") == "primary_to_secondary"
    selected_groups = form.getlist("groups")  # Get selected groups if any
    
    # Update word selection based on groups
    words = word_selector.choose_next_words(
        db, 
        nb_questions, 
        groups=selected_groups if selected_groups else None
    )
    
    session_id = session_manager.create_session(
        words=words,
        primary_to_secondary=primary_to_secondary,
        nb_questions=nb_questions
    )
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
    question = word.primary_text if quiz_session["primary_to_secondary"] else word.secondary_text
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_question.html",
        context={
            "word_to_translate": question,
            "question_id": question_id,
            "nb_questions": nb_questions,
            "russian_layout": russian_keyboard_layout(),
            "is_mobile_device": is_mobile(request.headers.get("user-agent", "")),
            "primary_to_secondary": quiz_session["primary_to_secondary"]
        }
    )

@router.post("/{session_id}/answer", name="quiz_answer")
async def submit_answer(session_id: str, request: Request, db: SessionDep):
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    form = await request.form()
    user_answer = form.get("answer")

    question_id = quiz_session["question_id"]
    session_word = quiz_session["words"][question_id]
    
    # Fetch fresh word data from database using the ID
    word = db.query(Word).filter(Word.id == session_word.id).first()
    if not word:
        return RedirectResponse("/quiz", status_code=303)
    
    is_correct = answer_handler.process_answer(
        db, word, user_answer, quiz_session["start_time"], quiz_session["primary_to_secondary"]
    )
    
    # Refresh the word object to get updated data
    db.refresh(word)
    
    # Store only the ID in the session
    quiz_session["words"][question_id] = word
    
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
    last_word: Word = quiz_session["words"][previous_question]
    last_answer = quiz_session["answers"][previous_question]
    question = last_word.primary_text if quiz_session["primary_to_secondary"] else last_word.secondary_text
    correct_answer = last_word.secondary_text if quiz_session["primary_to_secondary"] else last_word.primary_text

    
    return templates.TemplateResponse(
        request=request,
        name="quiz_answer.html",
        context={
            "word": question,
            "user_answer": last_answer,
            "correct_answer": correct_answer,
            "is_correct": last_answer == correct_answer,
            "success_count": last_word.success_count,
            "attempt_count": last_word.attempt_count,
        }
    )

@router.get("/{session_id}/summary", name="quiz_summary", response_class=HTMLResponse)
def quiz_summary(request: Request, session_id: str):
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    # Create word progress details
    word_progress = []
    for i, word in enumerate(quiz_session["words"]):
        word_progress.append({
            "primary_text": word.primary_text,
            "secondary_text": word.secondary_text,
            "success_rate": (word.success_count / word.attempt_count * 100) if word.attempt_count > 0 else 0,
            "success_count": word.success_count,
            "attempt_count": word.attempt_count,
            "current_answer": quiz_session["answers"][i],
            "is_correct": quiz_session["answers"][i] == (word.secondary_text if quiz_session["primary_to_secondary"] else word.primary_text)
        })
    
    return templates.TemplateResponse(
        request=request,
        name="quiz_summary.html",
        context={
            "score": quiz_session["score"],
            "nb_questions": len(quiz_session["words"]),
            "word_progress": word_progress,
            "group_id": session_id
        }
    )

@router.get("/", response_class=HTMLResponse)
async def quiz_home(request: Request, db: SessionDep):
    # Count available words
    nb_words_available = db.query(Word).count()
    
    return templates.TemplateResponse(
        "quiz_menu.html",
        {
            "request": request,
            "nb_words_available": nb_words_available
        }
    )
