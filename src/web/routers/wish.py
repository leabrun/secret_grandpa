from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from database.queries import insert_wish, select_wish_by_id, delete_wish
from utils import get_id_from_cookie, templates

router = APIRouter()


@router.get("/create/wish", response_class=HTMLResponse)
async def create_wish_page(request: Request):
    template = "create_wish.html"
    context = {"request": request}

    client_id = get_id_from_cookie(request)
    context["user_id"] = client_id

    return templates.TemplateResponse(template, context)


@router.post("/create/wish")
async def create_wish_request(request: Request,
                              wish_title: str = Form(...),
                              wish_url: str = Form(...)):
    client_id = get_id_from_cookie(request)

    if wish_url and not wish_url.startswith("https://"):
        wish_url = "https://"+wish_url

    await insert_wish(wish_title, wish_url, client_id)

    return RedirectResponse(f"/user/{client_id}", status_code=303)


@router.get("/delete/wish/{wish_id}")
async def delete_wish_request(request: Request,
                              wish_id: int):

    client_id = get_id_from_cookie(request)
    wish = await select_wish_by_id(wish_id)

    if not wish:
        return HTMLResponse(content="Wish not found", status_code=404)

    if client_id == wish.owner_id:
        await delete_wish(wish_id)

    return RedirectResponse(f"/user/{client_id}", status_code=303)
