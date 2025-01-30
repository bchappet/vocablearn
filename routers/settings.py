from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.database import SessionDep
from sqlmodel import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/settings", response_class=HTMLResponse)
async def get_settings(request: Request, db: SessionDep):
    statement = select(Settings)
    settings = db.exec(statement).first()
    return templates.TemplateResponse(
        "settings.html",
        {"request": request, "settings": settings}
    )

@router.post("/settings")
async def update_settings(
    db: SessionDep,
    direction: str = Form(...),
    questions_per_quiz: int = Form(...),
):
    # Delete all existing settings
    statement = select(Settings)
    existing_settings = db.exec(statement).all()
    for setting in existing_settings:
        db.delete(setting)
    db.commit()
    
    # Create new settings
    settings = Settings(
        nb_questions=questions_per_quiz
    )
    db.add(settings)
    db.commit()
    return RedirectResponse("/", status_code=303)
