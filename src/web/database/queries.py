from sqlalchemy import text, update
from typing import Optional
from random import shuffle

from .core import AsyncSessionLocal
from .models import Users, Teams, Members, Wishes
from utils import generate_team_code


# ----------- USERS -------------
async def select_user_by_id(id: int):
    async with AsyncSessionLocal() as asl:
        user_q = await asl.execute(text(f"SELECT * FROM users WHERE id={id}"))

        return user_q.first()


async def insert_user(id: int, name: str):
    async with AsyncSessionLocal() as asl:
        new_user = Users(id=id,
                         name=name)
        asl.add(new_user)
        await asl.commit()


# ----------- TEAMS -------------
async def select_team_by_id(id: str):
    async with AsyncSessionLocal() as asl:
        team_q = await asl.execute(text(f"SELECT * FROM teams WHERE id={id}"))

        return team_q.first()


async def select_team_by_code(code: str):
    async with AsyncSessionLocal() as asl:
        team_q = await asl.execute(text(f"SELECT * FROM teams \
                                        WHERE code='{code}'"))

        return team_q.first()


async def select_teams_by_user_id(id: int):
    async with AsyncSessionLocal() as asl:
        teams_q = await asl.execute(text(f"SELECT teams.title, teams.id \
                                         FROM teams \
                                         INNER JOIN members \
                                         ON teams.id = members.team_id \
                                         WHERE members.user_id={id} \
                                         ORDER BY teams.id DESC"))

        return teams_q.fetchall()


async def insert_team(title: str, owner_id: int):
    async with AsyncSessionLocal() as asl:
        team_code = generate_team_code()
        new_team = Teams(title=title,
                         owner_id=owner_id,
                         is_closed=False,
                         code=team_code)
        asl.add(new_team)
        await asl.commit()

        await insert_member(owner_id, new_team.id)


async def delete_team(id: int):
    async with AsyncSessionLocal() as asl:
        await asl.execute(text(f"DELETE FROM teams WHERE id={id}"))
        await asl.commit()


# ------------- MEMBERS -------------
async def insert_member(user_id: int, team_id: int):
    async with AsyncSessionLocal() as asl:
        new_member = Members(user_id=user_id,
                             team_id=team_id)
        asl.add(new_member)
        await asl.commit()


async def select_members_by_team_id(id: int):
    async with AsyncSessionLocal() as asl:
        members_q = await asl.execute(text(f"SELECT users.id, users.name \
                                           FROM users \
                                           INNER JOIN members \
                                           ON users.id = members.user_id \
                                           WHERE members.team_id={id}"))

        return members_q.fetchall()


async def select_member(user_id: int, team_id: int):
    async with AsyncSessionLocal() as asl:
        members_q = await asl.execute(text(f"SELECT * FROM members \
                                           WHERE user_id={user_id} \
                                           AND team_id={team_id}"))

        return members_q.fetchall()


async def delete_member(member_id: int, team_id: int):
    async with AsyncSessionLocal() as asl:
        await asl.execute(text(f"DELETE FROM members \
                               WHERE user_id={member_id} \
                               AND team_id={team_id}"))
        await asl.commit()


async def assign_members(id: int):
    async with AsyncSessionLocal.begin() as asl:
        members = await select_members_by_team_id(id)
        length = len(members)

        if length < 3:
            return False

        shuffle(members)

        for i in range(0, length):
            if i == length-1:
                await asl.execute(update(Members)
                                  .where(Members.team_id == id)
                                  .where(Members.user_id == members[i].id)
                                  .values(destiny=members[0].id))

                break

            await asl.execute(update(Members)
                              .where(Members.team_id == id)
                              .where(Members.user_id == members[i].id)
                              .values(destiny=members[i+1].id))

        await asl.execute(update(Teams)
                          .where(Teams.id == id)
                          .values(is_closed=True))

        await asl.commit()


async def get_destiny_name(user_id: int, team_id: int):
    async with AsyncSessionLocal.begin() as asl:
        destiny_q = await asl.execute(text(f"SELECT users.name \
                                           FROM members \
                                           INNER JOIN users \
                                           ON members.destiny = users.id \
                                           WHERE members.user_id={user_id} \
                                           AND members.team_id={team_id}"))
        destiny = destiny_q.first()

        return destiny.name


# ----------- WISHES -------------
async def select_wishes_by_owner_id(id: int):
    async with AsyncSessionLocal() as asl:
        wishes_q = await asl.execute(text(f"SELECT * FROM wishes \
                                          WHERE owner_id={id}"))

        return wishes_q.fetchall()


async def select_wish_by_id(id: int):
    async with AsyncSessionLocal() as asl:
        wishes_q = await asl.execute(text(f"SELECT * FROM wishes \
                                          WHERE id={id}"))

        return wishes_q.first()


async def insert_wish(title: str, url: Optional[str], id: int):
    async with AsyncSessionLocal() as asl:
        new_wish = Wishes(title=title,
                          url=url,
                          owner_id=id)
        asl.add(new_wish)
        await asl.commit()


async def delete_wish(id: int):
    async with AsyncSessionLocal() as asl:
        await asl.execute(text(f"DELETE FROM wishes WHERE id={id}"))
        await asl.commit()
