
import os
import re
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


@router.get("/mnemonic/{word}/{translation}", name='generate_mnemonic', response_class=HTMLResponse)
async def generate_mnemonic(request: Request, word: str, translation: str):

    def remove_think_tags(text):
        pattern = r'<think>.*?</think>'
        result = re.sub(pattern, '', text, flags=re.DOTALL)
        return result


    fpath = os.path.join('routers', 'quiz', 'ai', 'prompts','claude_generated_prompt.txt')
    api_key = os.environ["GROQ_API_KEY"]
    model_name = "deepseek-r1-distill-llama-70b"
    model = GroqModel(model_name=model_name,api_key=api_key)
    with open(fpath, encoding="utf8") as f:
        system_prompt = f.readlines()
        agent = Agent(model, system_prompt=system_prompt)
        result = await agent.run(f'Please give me some help to rembember the word {word} ({translation})')
        print(result.data)
        clean_result = remove_think_tags(result.data)

    return templates.TemplateResponse(
        "ai/mnemonic.html",
        {
            "request": request,
            "word": word,
            "translation": translation,
            "html_content": clean_result
        }
    )