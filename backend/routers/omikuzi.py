import requests
from fastapi import APIRouter, File
router = APIRouter()


@router.post(
    "/omikuzi",
    tags=["omikuzi"],
    summary="テキストからおみくじの生成",
    response_model=File,
)
async def gpt(text: str) -> File:
    pass
