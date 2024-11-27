from fastapi import APIRouter,UploadFile,Body
import os
from fastapi import APIRouter, HTTPException
from schemas.nft_schema import NFTMetadata
from services.nft_service import upload_to_pinata,get_balance

router = APIRouter()

@router.post(
    "/nft",
    tags=["NFT"],
    summary="画像のアップロードとNFTの発行",
    response_model=NFTMetadata,
)
async def mint_nft(upload_file: UploadFile
):
    image_url = await upload_to_pinata(upload_file)
    nft_metadata = NFTMetadata
    nft_metadata.name = upload_file.filename
    nft_metadata.description = "NFT with GOD により、生成されたおみくじです。"
    nft_metadata.image = image_url
    return nft_metadata


@router.get(
    "/nft/balance",
    tags=["NFT"],
    summary="NFTアカウントの残高確認",
)
async def balance():
    try:
        balance = get_balance()  # 残高を取得
        return balance  # 辞書を直接返す
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")