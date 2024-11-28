from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/app/static"))


@app.get("/", response_class=HTMLResponse)
async def home_page():
    with open("src/app/templates/home.html", "r") as file:
        return file.read()
