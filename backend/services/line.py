from fastapi import Cookie, Request
import httpx
from utils.config import get_line_client_id, get_line_client_secret, get_line_redirect_uri
from utils.jwt import decode_hs256

CLIENT_ID = get_line_client_id()
CLIENT_SECRET = get_line_client_secret()
REDIRECT_URI = get_line_redirect_uri()


async def get_token(code: str):
    url = "https://api.line.me/oauth2/v2.1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()


def get_user_id(id_token):
    decoded_token = decode_hs256(id_token, CLIENT_ID, CLIENT_SECRET)
    return decoded_token["sub"]


def get_user_id_from_cookie(id_token: str = Cookie(None)) -> str:
    decoded_token = decode_hs256(id_token, CLIENT_ID, CLIENT_SECRET)
    return decoded_token["sub"]


def get_profile(id_token):
    decoded_token = decode_hs256(id_token, CLIENT_ID, CLIENT_SECRET)
    return {
        "name": decoded_token["name"],
        "picture": decoded_token["picture"]
    }


async def get_profile_by_endpoint(id_token):
    url = "https://api.line.me/oauth2/v2.1/verify"
    data = {
        "id_token": id_token,
        "client_id": CLIENT_ID,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        response.raise_for_status()
        return response.json()
