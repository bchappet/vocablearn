from datetime import datetime
from models.database import SessionDep
from models.tables import Word, WordProgress

def process_answer(db: SessionDep, word: dict, user_answer: str, start_time: datetime, ru_to_en: bool) -> bool:
    is_correct = user_answer == word["answer"]
    response_time = (datetime.utcnow() - start_time).total_seconds()
    
    word_obj = (
        db.query(Word)
        .filter(
            Word.english == (word["question"] if ru_to_en else word["answer"]),
            Word.russian == (word["answer"] if ru_to_en else word["question"])
        )
        .first()
    )
    
    if word_obj:
        progress = WordProgress(
            word_id=word_obj.id,
            correct=is_correct,
            response_time=response_time,
            ru_to_en=ru_to_en
        )
        db.add(progress)
        db.commit()
    
    return is_correct
