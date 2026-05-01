from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from urllib.parse import urlencode
from starlette.requests import Request
import aiohttp
import re

from testoauth.core.settings import settingsjwt
from testoauth.core.aiohttp.setup import get_aiohttp_session

from .schemas import RedirectUrlToSteam
from .openid import get_steam_player_info

router = APIRouter(prefix="/auth", tags=["Auth"])

BACKEND_URL = "http://127.0.0.1:8000"


@router.get("/steam")
async def auth_steam():

    data = RedirectUrlToSteam(
        ns=settingsjwt.openid.ns,
        mode="checkid_setup",
        return_to=f"{BACKEND_URL}/auth/steam/callback",
        realm=BACKEND_URL,
        identity=settingsjwt.openid.identity,
        claimed_id=settingsjwt.openid.claimed_id,
    )

    params = data.model_dump(by_alias=True)
    steam_login_url = f"{settingsjwt.openid.base_url}?{urlencode(params)}"

    return RedirectResponse(url=steam_login_url)


@router.get("/steam/callback")
async def auth_steam_callback(
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    request: Request,
):
    params = dict(request.query_params)

    # Проверяем, что пользователь не отменил вход
    if params.get("openid.mode") != "id_res":
        raise HTTPException(status_code=400, detail="Auth failed or cancelled")

    # ---------------------------------------------------------
    # Верификация подписи через Steam
    # ---------------------------------------------------------
    validation_params = dict(params)
    validation_params["openid.mode"] = "check_authentication"

    # aiohttp: POST-запрос
    async with session.post(
        settingsjwt.openid.base_url,
        data=validation_params,  # form-data (application/x-www-form-urlencoded)
    ) as response:
        response_text = await response.text()

    if "is_valid:true" not in response_text:
        raise HTTPException(
            status_code=401,
            detail="Steam validation failed",
        )

    # ---------------------------------------------------------
    # Извлекаем SteamID64
    # ---------------------------------------------------------
    claimed_id = params.get("openid.claimed_id", "")

    match = re.search(r"/openid/id/(\d+)$", claimed_id)
    if not match:
        raise HTTPException(status_code=400, detail="Could not extract SteamID")

    steam_id = match.group(1)

    player_data = await get_steam_player_info(steam_id, session)

    print(player_data)

    return JSONResponse(content=player_data)
