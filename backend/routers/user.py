from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlmodel import Session
from cruds.user import create_user, get_user
from database import get_db
from models.user import User
from services.line import get_user_id, get_profile, get_user_id_from_cookie


router = APIRouter()


@router.get(
    "/users/me/profile",
    tags=["users"],
    summary="プロフィール情報取得",
)
async def login(id_token: str = Cookie(None)):
    if id_token:
        user_id = get_user_id(id_token)
        profile = get_profile(id_token)
        return { "id": user_id, **profile }
    return {"message": "No cookie received"}


@router.post(
    "/users/{user_id}",
    tags=["users"],
    summary="新規ユーザの作成",
    response_model=User,
    status_code=201
)
def create_user_endpoint(
    user_id: str = Depends(get_user_id_from_cookie),
    db: Session = Depends(get_db),
):
    existing_user = get_user(db, user_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(id=user_id, thread_id="thread_default")
    return create_user(db, user)
