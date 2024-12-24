from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from database.queries import (insert_team, select_team_by_id,
                              delete_team, select_members_by_team_id,
                              delete_member, get_destiny)
from utils import templates, get_id_from_cookie

router = APIRouter()


@router.get("/create/team", response_class=HTMLResponse)
async def create_team_page(request: Request):
    template = "create_team.html"
    context = {"request": request}

    return templates.TemplateResponse(template, context)


@router.post("/create/team")
async def create_team_request(request: Request,
                              team_title: str = Form(...)):
    client_id = get_id_from_cookie(request)
    await insert_team(team_title, client_id)

    return RedirectResponse("/home", status_code=303)


@router.get("/delete/team/{team_id}")
async def delete_team_request(request: Request,
                              team_id: int):

    client_id = get_id_from_cookie(request)
    team = await select_team_by_id(team_id)

    if not team:
        return HTMLResponse(content="Team not found", status_code=404)

    if client_id == team.owner_id:
        await delete_team(team_id)

    return RedirectResponse("/home", status_code=303)


@router.get("/team/{team_id}", response_class=HTMLResponse)
async def team_page(request: Request,
                    team_id: int):
    template = "team.html"
    context = {"request": request}

    is_owner = False
    client_id = get_id_from_cookie(request)

    team = await select_team_by_id(team_id)

    if not team:
        return HTMLResponse(content="Team not found", status_code=404)

    if team.owner_id == client_id:
        is_owner = True

    members = await select_members_by_team_id(team_id)

    if team.is_closed:
        client_destiny = await get_destiny(client_id, team_id)
        context["destiny"] = client_destiny

    context["team"] = team
    context["members"] = members
    context["is_owner"] = is_owner

    return templates.TemplateResponse(template, context)


@router.get("/delete/member/{member_id}/{team_id}")
async def delete_member_request(request: Request,
                                member_id: int,
                                team_id: int):
    client_id = get_id_from_cookie(request)
    team = await select_team_by_id(team_id)

    if client_id == team.owner_id and client_id != member_id:
        await delete_member(member_id, team_id)

    return RedirectResponse(f"/team/{team_id}", status_code=303)


@router.get("/quit/team/{team_id}")
async def quit_team_request(request: Request,
                            team_id: int):
    client_id = get_id_from_cookie(request)
    team = await select_team_by_id(team_id)

    if team:
        await delete_member(client_id, team_id)

    return RedirectResponse("/home", status_code=303)
