from typing import List, Optional
from sqlalchemy import func
from models.database import SessionDep
from models.tables import Word

def choose_next_words(
    db: SessionDep, 
    nb_words_to_choose: int, 
    groups: Optional[List[str]] = None
) -> List[Word]:
    """
    Returns a list of random words from the database.
    
    Args:
        db: Database session
        nb_words_to_choose: Number of words to return
        groups: Optional list of group IDs to filter by
    
    Returns:
        List of randomly selected Word objects
    """
    query = db.query(Word)
    
    # If groups are specified, filter words by those groups
    if groups and len(groups) > 0:
        query = query.filter(Word.group_id.in_(groups))
    
    words = query.order_by(func.random()).limit(nb_words_to_choose).all()
    return words
