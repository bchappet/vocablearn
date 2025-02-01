from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.database import SessionDep
from models.tables import Word
from sqlalchemy import func

router = APIRouter(
    prefix="/progress",
    tags=["stats"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def read_stats(request: Request, db: SessionDep):
    # Get total number of words
    total_words = db.query(Word).count()
    
    # Get mastered words (>3 attempts and >90% success rate)
    mastered_words = db.query(Word).filter(
        Word.attempt_count >= 3,
        Word.success_count / Word.attempt_count >= 0.9
    ).count()
    
    return templates.TemplateResponse(
        request=request,
        name="stats.html",
        context={
            "total_words": total_words,
            "mastered_words": mastered_words
        }
    ) 