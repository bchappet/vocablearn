from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from utils.web import is_mobile
from utils.web import russian_keyboard_layout


router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/", name="read_keyboard", response_class=HTMLResponse)
async def read_keyboard(request: Request) -> HTMLResponse:
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




@router.get("/keyboard", name="keyboard_settings", response_class=HTMLResponse)
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