from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
from dotenv import load_dotenv

from database.core import init_db
from database.queries import select_teams_by_user_id
from routers import system, team, user, wish
from utils import templates, get_id_from_cookie

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/web/static"))

app.include_router(system.router)
app.include_router(team.router)
app.include_router(user.router)
app.include_router(wish.router)


@app.get("/", response_class=HTMLResponse)
async def start_page(request: Request):
    template = "start.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)


@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    template = "home.html"
    context = {"request": request}

    client_id = get_id_from_cookie(request)
    teams = await select_teams_by_user_id(client_id)
    context["teams"] = teams

    return templates.TemplateResponse(template, context)


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run(app="main:app",
                host="0.0.0.0",
                port=8000,
                reload=True)
