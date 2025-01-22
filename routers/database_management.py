from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from models.populate_db import populate_from_csv

router = APIRouter()

@router.get("/reset_database")
async def reset_database(request: Request):
    populate_from_csv(csv_path="models/words_csv/words.csv", erase_first=True)
    return RedirectResponse(url="/", status_code=303)
