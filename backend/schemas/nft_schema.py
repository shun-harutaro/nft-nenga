from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class NFTMetadata(BaseModel):
    name: str
    description: Optional[str] = None
    image: HttpUrl  # IPFS URLなど
    attributes: Optional[List[dict]] = None  # OpenSeaの属性形式など
