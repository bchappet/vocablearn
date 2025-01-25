from typing import Dict
from datetime import datetime
import uuid

# In-memory session storage (replace with database in production)
sessions: Dict[str, dict] = {}

def create_session(words: list) -> str:
    session_id = str(uuid.uuid4())
    quiz_session = {
        "session_id": session_id,
        "question_id": 0,
        "words": words,
        "answers": [],
        "score": 0,
        "start_time": datetime.utcnow()
    }
    sessions[session_id] = quiz_session
    return session_id

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
