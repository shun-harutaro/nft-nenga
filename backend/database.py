#import ssl
from typing import AsyncGenerator#, Dict

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

#from config import get_db_cert_path, get_db_object


def create_dev_async_engine():
    from sqlalchemy.engine.url import URL

    url = URL.create(
        drivername="mysql+aiomysql",
        username="root",
        host="mysql",
        database="dev",
        query={"charset": "utf8"},
    )
    async_engine = create_async_engine(url, echo=True, future=True)
    return async_engine


"""
def create_prod_async_engine():
    from sqlalchemy.engine.url import URL

    DB_OBJECT: Dict[str, str] = get_db_object()
    DB_CERT_PATH = get_db_cert_path()
    ssl_context = ssl.create_default_context(cafile=DB_CERT_PATH)
    url = URL.create(
        drivername="mysql+aiomysql",
        username=DB_OBJECT["username"],
        password=DB_OBJECT["password"],
        host=DB_OBJECT["host"],
        database=DB_OBJECT["database"],
        query={"charset": "utf8"},
    )
    async_engine = create_engine(
        url, connect_args={"ssl": ssl_context}, echo=True, future=True
    )
    return async_engine
"""


# 環境に応じたエンジンを作成
async_engine = create_dev_async_engine()# if IS_DEV_MODE else create_prod_async_engine()

# 非同期セッションの作成
async_session = AsyncSession(async_engine)


# SQLModelの基底クラス
class Base(SQLModel):
    pass


# データベースセッションを提供するジェネレーター関数
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session as session:
        yield session
