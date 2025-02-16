from datetime import datetime
from models.database import SessionDep
from models.tables import Word

def process_answer(db: SessionDep, word: Word, user_answer: str,
                   start_time: datetime, primary_to_secondary: bool) -> bool:
    """Process a user's answer to a quiz question and update the word statistics.

    """
    
    correct_answer = word.secondary_text if primary_to_secondary else word.primary_text
    is_correct = user_answer == correct_answer.rstrip().lower()
    response_time = (datetime.utcnow() - start_time).total_seconds()
    
    # Update word statistics
    word.attempt_count += 1
    if is_correct:
        word.success_count += 1
    word.mastery = word.success_count / word.attempt_count
    
    db.commit()
    
    return is_correct
