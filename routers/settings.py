from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.database import SessionDep
from sqlmodel import select
from utils.web import is_mobile, russian_keyboard_layout

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/settings", response_class=HTMLResponse)
async def get_settings(request: Request, db: SessionDep):
    return templates.TemplateResponse(
        "settings.html",
        {"request": request}
    )

@router.get("/settings/keyboard", name="keyboard_settings", response_class=HTMLResponse)
async def keyboard_settings(request: Request) -> HTMLResponse:
    user_agent = request.headers.get("user-agent", "")
    is_mobile_device = is_mobile(user_agent)
    
    russian_layout = russian_keyboard_layout()
    
    template_name = "keyboard_mobile.html" if is_mobile_device else "keyboard_desktop.html"
    return templates.TemplateResponse(
        template_name,
        {
            "request": request,
            "russian_layout": russian_layout
        }
    )

@router.post("/settings")
async def update_settings():
    return RedirectResponse("/", status_code=303)
