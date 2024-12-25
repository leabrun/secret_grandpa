from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from typing import Optional

from database.queries import (select_user_by_id,
                              insert_user,
                              update_user,
                              select_team_by_code,
                              select_team_by_id,
                              insert_member,
                              select_member,
                              assign_members)
from utils import serializer, get_id_from_cookie

router = APIRouter()


@router.post("/set/user")
async def set_user(request: Request,
                   response: Response,
                   data: dict):
    def set_cookie(client_id: int):
        cookie_data = serializer.dumps(client_id)
        response.set_cookie(key="client_id",
                            value=cookie_data,
                            httponly=True)

        return True

    async def save_user(user_id: int, user_name: str,
                        photo_url: Optional[str]):
        user = await select_user_by_id(user_id)

        if not user:
            await insert_user(user_id, user_name, photo_url)

        elif user.name != user_name or user.photo != photo_url:
            await update_user(user_id, user_name, photo_url)

        return True

    async def set_member(user_id: int, team_code: str):
        team = await select_team_by_code(team_code)

        if team and not team.is_closed:
            member = await select_member(user_id, team.id)

            if not member:
                await insert_member(user_id, team.id)

        return True

    client_id = data.get("user_id")
    client_name = data.get("user_name")
    photo_url = data.get("photo_url")
    team_code = data.get("team_code")

    if client_id and client_name:
        set_cookie(client_id)
        await save_user(client_id, client_name, photo_url)

        if team_code:
            await set_member(client_id, team_code)

        return {"message": f"{client_name} was initialized!"}

    else:
        return {"message": "Auth Error! Try again..."}


@router.get("/assign/{team_id}")
async def assignment(request: Request,
                     team_id: int,):
    client_id = get_id_from_cookie(request)
    team = await select_team_by_id(team_id)

    if team and team.owner_id == client_id and not team.is_closed:
        await assign_members(team_id)

    return RedirectResponse(f"/team/{team_id}", status_code=303)
