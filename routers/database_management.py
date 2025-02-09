from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from models.populate_db import populate_all_csvs

router = APIRouter()

@router.get("/reset_database")
async def reset_database(request: Request):
    # populate_all_csvs(csv_path="models/words_csv", erase_first=True)
    populate_all_csvs(csv_path="models/words_csv/cours8.csv", erase_first=False)
    return RedirectResponse(url="/", status_code=303)
