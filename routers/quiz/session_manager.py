from typing import Dict, List
from datetime import datetime
from models.database import SessionDep
from . import word_selector
from .word_selector import ChoosenReason
import uuid

# In-memory session storage (replace with database in production)
sessions: Dict[str, dict] = {}

def _create_session(words: list, primary_to_secondary: bool, nb_questions: int, selected_groups: List[str],
                    choosen_reason: List[ChoosenReason]) -> str:
    session_id = str(uuid.uuid4())
    quiz_session = {
        "session_id": session_id,
        "question_id": 0,
        "words": words,  # These are now the actual Word objects from the database
        "choosen_reason": choosen_reason,  # why we choose those words
        "answers": [],
        "is_correct": [],
        "score": 0,
        "start_time": datetime.utcnow(),
        "primary_to_secondary": primary_to_secondary,
        "nb_questions": nb_questions,
        "selected_groups": selected_groups,
    }
    sessions[session_id] = quiz_session
    return session_id

def start_new_session(db : SessionDep, nb_questions: int, primary_to_secondary: bool, selected_groups: List[str]) -> str:
    # Update word selection based on groups
    words, choosen_reason = word_selector.choose_next_words(db, nb_questions, 
        groups=selected_groups if selected_groups else None
    )

    return _create_session( words, primary_to_secondary, nb_questions, selected_groups, choosen_reason)
    


def get_session(session_id: str) -> dict:
    return sessions.get(session_id)

def update_session_answer(session_id: str, is_correct: bool, user_answer: str) -> None:
    session = sessions.get(session_id)
    if session:
        if is_correct:
            session["score"] += 1
        session["question_id"] += 1
        session["answers"].append(user_answer)
        session["start_time"] = datetime.utcnow()
