from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aiohttp

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from testoauth.core.settings import settingscors
from testoauth.core.aiohttp.setup import aiohttp_session_manager

from testoauth.auth.controller import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    await aiohttp_session_manager.start()

    yield

    await aiohttp_session_manager.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settingscors.urls,  # pyright:ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
