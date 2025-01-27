from datetime import datetime
from models.database import SessionDep
from models.tables import Word, WordProgress

def process_answer(db: SessionDep, word: Word, user_answer: str, start_time: datetime, ru_to_en: bool) -> bool:
    is_correct = user_answer == (word.english if ru_to_en else word.russian)
    response_time = (datetime.utcnow() - start_time).total_seconds()
    word.attempt_count += 1
    word.success_count += is_correct

    progress = WordProgress(
        word_id=word.id,
        correct=is_correct,
        response_time=response_time,
        ru_to_en=ru_to_en
    )
    db.add(progress)
    db.commit()
    
    return is_correct
