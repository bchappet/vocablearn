from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


router = APIRouter(
    prefix="/keyboard",
    tags=["keyboard"],
)

templates = Jinja2Templates(directory="templates")

def is_mobile(user_agent: str) -> bool:
    """Check if the user agent is from a mobile device."""
    mobile_patterns = [
        'Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone',
        'webOS', 'BlackBerry', 'Samsung', 'Opera Mini'
    ]
    return any(pattern.lower() in user_agent.lower() for pattern in mobile_patterns)


@router.get("/", name="read_keyboard", response_class=HTMLResponse)
async def read_keyboard(request: Request) -> HTMLResponse:
    user_agent = request.headers.get("user-agent", "")
    is_mobile_device = is_mobile(user_agent)

    # Define keyboard layouts
    russian_layout = {
        'row1': ['ё', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
        'row2': ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ'],
        'row3': ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
        'row4': ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.']
    }
    
    russian_shift_layout = {
        'row1': ['Ё', '!', '"', '№', ';', '%', ':', '?', '*', '(', ')', '_', '+'],
        'row2': ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ'],
        'row3': ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э'],
        'row4': ['Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', ',']
    }
    
    template_name = "keyboard_mobile.html" if is_mobile_device else "keyboard_desktop.html"
    return templates.TemplateResponse(
        template_name,
        {
            "request": request,
            "russian_layout": russian_layout,
            "russian_shift_layout": russian_shift_layout
        }
    )