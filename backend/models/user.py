from typing import Optional,List,TYPE_CHECKING
from sqlmodel import Field, SQLModel,Relationship
from datetime import datetime
from models.nft import Nft

if TYPE_CHECKING:
    from models.nft import Nft
class User(SQLModel, table=True):
    id: str = Field(
        ..., primary_key=True, index=True, max_length=33,
        schema_extra={'pattern': r"^U[a-f0-9]{32}$"}
    )
    thread_id: str = Field(
        ..., max_length=45, schema_extra={'pattern': r"^thread_"}
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": lambda: datetime.now()}
    )
    nfts: Optional[List["Nft"]] = Relationship(back_populates="user")
