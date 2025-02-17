
import os
from fastapi import APIRouter, Request 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .. import session_manager
from pydantic_ai.models.groq import GroqModel
from pydantic_ai import Agent

router = APIRouter(
    prefix="/quiz/ai",
    tags=["quiz/ai"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/{session_id}", name='quiz_ai', response_class=HTMLResponse)
async def quiz_ai(request: Request, session_id: str):
    """user click on ai option in quiz answer screen"""
    quiz_session = session_manager.get_session(session_id)
    if not quiz_session:
        return RedirectResponse("/quiz", status_code=303)
    
    question_id = quiz_session['question_id']-1
    focus_word = quiz_session['words'][question_id]
    return templates.TemplateResponse(
        "ai/quiz_ai.html",
        {
            "request": request,
            "focus_word_primary": focus_word.primary_text,
            "focus_word_secondary": focus_word.secondary_text,
        }
    )


@router.get("/mnemonic/{word}", name='generate_mnemonic', response_class=HTMLResponse)
async def generate_mnemonic(request: Request, word: str):
    api_key = os.environ["GROQ_API_KEY"]
    model = GroqModel(model_name="mixtral-8x7b-32768",api_key=api_key)
    agent = Agent(model, system_prompt='You are a russian language teacher. You role is to help the user to remember russian vocabulary.')
    result = await agent.run(f'Please give me a mnemonic to remember the word {word}')
    print(result.data)
    return templates.TemplateResponse(
        "ai/mnemonic.html",
        {
            "request": request,
            "word" : word,
            "answer": result.data
        }

    )