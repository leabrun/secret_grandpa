from fastapi import Request
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer
import string
import random
import os

templates = Jinja2Templates(directory="src/web/templates")

serializer = URLSafeSerializer(os.getenv("SESSION_KEY"))


def get_id_from_cookie(request: Request) -> str:
    hash_id = request.cookies.get("client_id")
    id = serializer.loads(hash_id)

    return id


def generate_team_code():
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(10))
