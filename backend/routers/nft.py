from fastapi import APIRouter, UploadFile, Depends
from typing import List, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, HTTPException
from database import get_db
from schemas.nft_schema import NFTMetadata
from services.nft_service import (
    upload_image_to_pinata,
    get_balance,
    upload_metadata_to_pinata,
    mint_nft,
    get_metadata_from_transaction,
    create_metadata,
    generate_name_with_user
)
from services.line import get_user_id_from_cookie
from utils.config import (
    get_nft_private_key
)
from models.nft import Nft
import cruds.nft as nft_crud
from services.line import get_user_id_from_cookie
from utils.query import get_nfts_image_and_time_by_user_id

NFT_PRIVATE_KEY = get_nft_private_key()

router = APIRouter()


@router.post(
    "/nft",
    tags=["NFT"],
    summary="画像のアップロードとNFTの発行"
)

async def mint(upload_file: UploadFile,
               user_id: str = Depends(get_user_id_from_cookie),
               db: AsyncSession = Depends(get_db)
               ):
    image_url = await upload_image_to_pinata(upload_file)
    nft_metadata = create_metadata(
        filename=upload_file.filename, image_url=image_url)
    metadata_url = upload_metadata_to_pinata(nft_metadata)
    tx_receipt = mint_nft(metadata_url, NFT_PRIVATE_KEY)
    tx_hash = tx_receipt.transactionHash.hex()
    try:
        token_id_hex = tx_receipt.logs[0]["topics"][3]
        token_id = int(token_id_hex.hex(), 16)
    except (KeyError, IndexError) as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve token ID: {str(e)}")
    response_data = {
        "name": nft_metadata.name,
        "description": nft_metadata.description,
        "image": nft_metadata.image,
        "attributes": nft_metadata.attributes,
        "transactionHash": tx_hash,
        "tokenId": token_id
    }

    existing_nft = await nft_crud.get_nft(db, tx_hash)
    if existing_nft:
        raise HTTPException(status_code=400, detail="NFT already exists")
    nft = Nft(id=tx_hash, user_id=user_id)
    await nft_crud.create_nft(db, nft)
    return response_data


@router.get(
    "/nft/metadata/{tx_hash}",
    tags=["NFT"],
    summary="トランザクションハッシュからメタデータと画像を取得",
)
async def get_nft_metadata(tx_hash: str):
    try:
        result = get_metadata_from_transaction(tx_hash)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=404, detail="User not found")


@router.get(
    "/nft/balance",
    tags=["NFT"],
    summary="NFTアカウントの残高確認",
)
async def balance():
    try:
        balance = get_balance()
        return balance
    except Exception as e:
        raise HTTPException(
            status_code=404, detail="NFT account not found")


@router.get(
    "/nft/users",
    tags=["NFT"],
    summary="特定のユーザーのNFT画像URLと作成日時を取得",
    response_model=List[Dict[str, str]]
)
async def get_nfts_by_user_endpoint(
    user_id: str = Depends(get_user_id_from_cookie),
    db: AsyncSession = Depends(get_db),
):
    nfts = await get_nfts_image_and_time_by_user_id(db, user_id)
    if not nfts:
        raise HTTPException(
            status_code=404, detail="No NFTs found for the given user ID")
    return nfts
