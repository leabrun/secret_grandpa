from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from database.queries import select_user_by_id, select_wishes_by_owner_id
from utils import templates, get_id_from_cookie

router = APIRouter()


@router.get("/user/{user_id}", response_class=HTMLResponse)
async def user_page(request: Request,
                    user_id: int):
    template = "user.html"
    context = {"request": request}
    is_owner = False

    client_id = get_id_from_cookie(request)

    if client_id == user_id:
        is_owner = True

    user = await select_user_by_id(user_id)

    if not user:
        return HTMLResponse(content="User not found", status_code=404)

    wishes = await select_wishes_by_owner_id(user_id)

    if not is_owner:
        user_name = user.name
        context["user_name"] = user_name

    context["wishes"] = wishes
    context["is_owner"] = is_owner

    return templates.TemplateResponse(template, context)
