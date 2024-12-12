from contextlib import asynccontextmanager
from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware

from routers import gpt, location, auth, nft, user,nft_database
from utils.config import check_env_variables


@asynccontextmanager
async def lifespan(app: FastAPI):
    check_env_variables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan, root_path="/api")
app.include_router(location.router)
app.include_router(gpt.router)
app.include_router(auth.router)
app.include_router(nft.router)
app.include_router(user.router)
app.include_router(nft_database.router)

"""
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
