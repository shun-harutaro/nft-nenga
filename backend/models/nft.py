from typing import Optional, List,TYPE_CHECKING
from sqlmodel import Field, SQLModel,Relationship
from datetime import datetime
if TYPE_CHECKING:
    from models.user import User

class Nft(SQLModel, table=True):
    nft_id: str = Field(
        ..., primary_key=True, index=True, max_length=100,
    )
    user_id: str = Field(foreign_key="user.id", max_length=33)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": lambda: datetime.now()}
    )
    user : Optional["User"] = Relationship(back_populates="nfts")