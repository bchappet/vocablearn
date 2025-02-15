from typing import List, Optional
from sqlalchemy import func
from models.database import SessionDep
from models.tables import Word
import random


def select_words(words: List[Word], nb_words_to_choose: int) -> List[Word]:
    """
    Select half:
    - Words never shown
    - Words with low mastery
    """
    words = words.copy()
    random.shuffle(words)
    never_shown = [w for w in words if w.attempt_count == 0]
    nb_never_shown = min(nb_words_to_choose//2, len(never_shown))
    never_shown = never_shown[:nb_never_shown]
    print(f"{nb_never_shown=} {never_shown}")

    low_mastery = []
    for word in words:
        if word.attempt_count > 3 and word.mastery < 0.75:
            low_mastery.append(word)

    nb_low_mastery = min(nb_words_to_choose//4, len(low_mastery))
    low_mastery = low_mastery[:nb_low_mastery]
    print(f"{nb_low_mastery=} {low_mastery}")

    nb_rest_of_the_words = nb_words_to_choose-(nb_low_mastery+nb_never_shown)
    result = never_shown + low_mastery
    rest_of_the_words = [w for w in words if w not in result]
    rest_of_the_words = rest_of_the_words[:nb_rest_of_the_words]
    print(f"{nb_rest_of_the_words=} {rest_of_the_words}")

    result += rest_of_the_words
    return result


def choose_next_words( db: SessionDep, nb_words_to_choose: int,
                       groups: Optional[List[str]] = None) -> List[Word]:
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
    
    all_words = query.all()
    words = select_words(all_words, nb_words_to_choose) 
    
    return words
