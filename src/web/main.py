from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .database.core import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/web/static"))
templates = Jinja2Templates(directory="src/web/templates")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: AsyncSession = Depends(get_db)):
    template = "home.html"
    context = {"request": request}

    res = await db.execute(text("SELECT title FROM teams"))
    teams = res.fetchall()

    context["teams"] = teams

    return templates.TemplateResponse(
        template, context
    )
