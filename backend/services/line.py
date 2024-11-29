import requests
import httpx
from utils.config import get_line_client_id, get_line_client_secret

CLIENT_ID = get_line_client_id()
CLIENT_SECRET = get_line_client_secret()


async def get_token(code: str):
    url = "https://api.line.me/oauth2/v2.1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8000/auth/callback",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()


def get_profile(id_token):
    # LINE API の IDトークン検証エンドポイント
    url = "https://api.line.me/oauth2/v2.1/verify"

    # リクエストのペイロード
    data = {
        "id_token": id_token,  # 取得済みのIDトークン
        "client_id": CLIENT_ID,  # LINE DevelopersコンソールのチャンネルID
    }

    response = requests.post(url, data=data)
    return response.json()
