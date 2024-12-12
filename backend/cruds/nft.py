from sqlmodel.ext.asyncio.session import AsyncSession
from models.nft import Nft
from typing import Optional


async def create_nft(db: AsyncSession, nft: Nft) -> Nft:
    db.add(nft)
    await db.commit()
    await db.refresh(nft)
    return nft


async def get_nft(db: AsyncSession, nft_id: str) -> Optional[Nft]:
    return await db.get(Nft, nft_id)


async def update_nft(db: AsyncSession, nft: Nft) -> Nft:
    db.add(nft)
    await db.commit()
    await db.refresh(nft)
    return nft


async def delete_nft(db: AsyncSession, nft: Nft) -> None:
    await db.delete(nft)
    await db.commit()
