from pydantic import BaseModel, ConfigDict
from typing import List


class RedirectUrlToSteam(BaseModel):

    model_config = ConfigDict(
        # Автоматически добавляем префикс "openid." ко всем полям
        alias_generator=lambda field_name: f"openid.{field_name}",
        # Позволяет создавать модель, используя обычные имена (без openid.)
        populate_by_name=True,
    )

    ns: str
    mode: str
    return_to: str
    realm: str
    identity: str
    claimed_id: str


# class ResponceSteamQueryParams(BaseModel):
