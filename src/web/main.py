from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
import asyncio

from database.core import get_db, init_db
from database.models import Teams

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/web/static"))
templates = Jinja2Templates(directory="src/web/templates")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: AsyncSession = Depends(get_db)):
    template = "home.html"
    context = {"request": request}

    res = await db.execute(text("SELECT title, id FROM teams"))
    teams = res.fetchall()

    context["teams"] = teams

    return templates.TemplateResponse(
        template, context
    )


@app.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
async def create_team(team_title: str = Form(...),
                      db: AsyncSession = Depends(get_db)):
    new_team = Teams(title=team_title, owner="me", is_closed=False)
    db.add(new_team)
    await db.commit()

    return RedirectResponse("/", status_code=303)


@app.get("/join", response_class=HTMLResponse)
async def join_page(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})


@app.post("/join")
async def join_team(team_number: str = Form(...),
                      db: AsyncSession = Depends(get_db)):
    # some

    return RedirectResponse("/", status_code=303)


@app.get("/team/{id}", response_class=HTMLResponse)
async def team_page(request: Request, id: int, db: AsyncSession = Depends(get_db)):
    template = "team.html"
    context = {"request": request}

    res = await db.execute(text(f"SELECT title FROM teams WHERE id={id}"))
    team = res.first()

    if not team:
        return HTMLResponse(content="Team not found", status_code=404)
    
    context["team"] = team
    
    return templates.TemplateResponse(
        template, context
    )


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run(app="main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
    )
