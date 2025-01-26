from typing import List
from sqlalchemy import func
from models.database import SessionDep
from models.tables import Word, Settings

def choose_next_words(db: SessionDep, nb_words_to_choose: int) -> List[dict]:
    """
    Returns a list of random words from the database.
    Each word is a dictionary containing 'id', 'question' and 'answer'.
    """
    words = db.query(Word).order_by(func.random()).limit(nb_words_to_choose).all()
    settings = db.query(Settings).first()
    return [{
        "id": word.id,
        "question": word.russian if settings.ru_to_en else word.english,
        "answer": word.english if settings.ru_to_en else word.russian
    } for word in words]
