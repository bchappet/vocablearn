from typing import List, Optional, Tuple
from sqlalchemy import func
from models.database import SessionDep
from models.tables import Word
import random
from enum import Enum
from enum import auto
from dataclasses import dataclass

class ChoosenReasonType(Enum):
    NEW = auto()
    TO_WORK = auto()
    RANDOM = auto()

@dataclass
class ChoosenReason:
    type : ChoosenReasonType
    details : str


def select_words(words: List[Word], nb_words_to_choose: int) -> Tuple[List[Word], List[ChoosenReason]]:
    """
    Select half:
    - Words never shown
    - Words with low mastery
    """
    words = words.copy()
    random.shuffle(words)

    choosen_reason = []

    # new
    never_shown = [w for w in words if w.attempt_count == 0]
    nb_never_shown = min(nb_words_to_choose//2, len(never_shown))
    never_shown = never_shown[:nb_never_shown]
    for w in never_shown:
        reason = ChoosenReason(ChoosenReasonType.NEW, "New word !")
        choosen_reason.append(reason)
    print(f"{nb_never_shown=} {never_shown}")

    # to work
    low_mastery = []
    for word in words:
        if word.attempt_count > 3 and word.mastery < 0.75:
            low_mastery.append(word)

    nb_low_mastery = min(nb_words_to_choose//4, len(low_mastery))
    low_mastery = low_mastery[:nb_low_mastery]
    for w in low_mastery:
        reason = ChoosenReason(ChoosenReasonType.TO_WORK, 
                               f"Need to work this word because you succeed {w.success_count} out of {w.attempt_count}.")
        choosen_reason.append(reason)
    print(f"{nb_low_mastery=} {low_mastery}")

    # rest is random
    nb_rest_of_the_words = nb_words_to_choose-(nb_low_mastery+nb_never_shown)
    result = never_shown + low_mastery
    rest_of_the_words = [w for w in words if w not in result]
    rest_of_the_words = rest_of_the_words[:nb_rest_of_the_words]
    for w in rest_of_the_words:
        reason = ChoosenReason(ChoosenReasonType.RANDOM,"random")
        choosen_reason.append(reason)
    print(f"{nb_rest_of_the_words=} {rest_of_the_words}")


    result += rest_of_the_words
   
    return result,choosen_reason


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
    words, choosen_reason = select_words(all_words, nb_words_to_choose) 
    
    return words, choosen_reason
