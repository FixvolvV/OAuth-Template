import aiohttp

from testoauth.core.settings import settingsjwt


async def get_steam_player_info(steam_id: str, session: aiohttp.ClientSession) -> dict:
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": settingsjwt.openid.api_key,
        "steamids": steam_id,
    }

    # aiohttp: GET-запрос
    async with session.get(url, params=params) as response:
        data = await response.json()

    players = data.get("response", {}).get("players", [])
    if players:
        return players[0]
    return {}
