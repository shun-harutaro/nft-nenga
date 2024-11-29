from fastapi import APIRouter
import secrets
from urllib.parse import urlencode

from fastapi.responses import RedirectResponse
from utils.config import get_line_client_id
from services.line import get_token

router = APIRouter()
CLIENT_ID = get_line_client_id()


@router.get("/auth/login")
async def login():
    state = secrets.token_urlsafe(16)
    # request.session["state"] = state
    base_url = "https://access.line.me/oauth2/v2.1/authorize"
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": "http://localhost:8000/auth/callback",
        "state": state,
        "scope": "profile openid",
    }
    redirect_url = f"{base_url}?{urlencode(params)}"
    return RedirectResponse(url=redirect_url)


@router.get("/auth/callback")
async def auth_callback(code: str, state: str):
    # TODO stateの検証
    token_response = await get_token(code)

    return {"state": state, "res": token_response}
