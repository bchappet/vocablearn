from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.database import SessionDep
from sqlmodel import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/settings", response_class=HTMLResponse)
async def get_settings(request: Request, db: SessionDep):
    return templates.TemplateResponse(
        "settings.html",
        {"request": request}
    )

@router.post("/settings")
async def update_settings():
    return RedirectResponse("/", status_code=303)
