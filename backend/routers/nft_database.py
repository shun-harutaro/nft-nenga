from fastapi import APIRouter, Cookie, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from database import get_db
from models.nft import Nft
import cruds.nft as nft_crud
from services.line import get_user_id, get_profile, get_user_id_from_cookie

router = APIRouter()


@router.get(
    "/nft-database/",
    tags=["NFT"],
    summary="nft-idの取得",
    response_model=Nft,
)
async def get_nft(
    nft_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    nft = await nft_crud.get_nft(db, nft_id)
    if nft is None:
        raise HTTPException(status_code=404, detail="Nft not found")
    return nft


@router.post(
    "/nft-add",
    tags=["NFT"],
    summary="NFTをデータベースに追加する",
    response_model=Nft,
    status_code=201,
)
async def create_nft_endpoint(
    nft_id: str = Query(...),
    user_id: str = Depends(get_user_id_from_cookie),
    db: AsyncSession = Depends(get_db),
):
    existing_nft = await nft_crud.get_nft(db, nft_id)
    if existing_nft:
        raise HTTPException(status_code=400, detail="Nft already exists")
    nft = Nft(nft_id=nft_id,user_id=user_id)
    return await nft_crud.create_nft(db, nft)


@router.delete(
    "/nft_delete",
    tags=["NFT"],
    summary="NFTの削除",
)
async def delete_nft(
    nft_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    nft = await nft_crud.get_nft(db, nft_id)
    if nft is None:
        raise HTTPException(status_code=404, detail="NFT not found")
    return await nft_crud.delete_nft(db, nft)
