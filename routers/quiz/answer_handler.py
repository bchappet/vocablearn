from datetime import datetime
from models.database import SessionDep
from models.tables import Word

def process_answer(db: SessionDep, word: Word, user_answer: str,
                   start_time: datetime, primary_to_secondary: bool) -> bool:
    """Process a user's answer to a quiz question and update the word statistics.

    Parameters
    ----------
    db : SessionDep
        Database session dependency for database operations
    word : Word
        The word object being tested
    user_answer : str
        The answer provided by the user
    start_time : datetime
        The time when the question was presented to the user
    primary_to_secondary : bool
        Direction of translation. If True, translating from primary to secondary language

    Returns
    -------
    bool
        True if the answer was correct, False otherwise

    Notes
    -----
    This function:
    - Validates the user's answer
    - Records response time
    - Updates word statistics (attempt_count and success_count)
    - Creates a WordProgress entry for the attempt
    - Commits changes to the database
    """
    
    correct_answer = word.secondary_text if primary_to_secondary else word.primary_text
    is_correct = user_answer == correct_answer
    response_time = (datetime.utcnow() - start_time).total_seconds()
    
    # Update word statistics
    word.attempt_count += 1
    if is_correct:
        word.success_count += 1
    
    db.commit()
    
    return is_correct
