from typing import List
from sqlalchemy import func
from models.database import SessionDep
from models.tables import Word, Settings

def choose_next_words(db: SessionDep, nb_words_to_choose: int) -> List[Word]:
    """
    Returns a list of random words from the database.
    """
    words = db.query(Word).order_by(func.random()).limit(nb_words_to_choose).all()
    return words
