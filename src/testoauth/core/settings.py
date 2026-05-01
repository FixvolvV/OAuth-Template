from pathlib import Path
from typing import List

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class OpenIDConfig(BaseModel):

    base_url: str
    ns: str = "http://specs.openid.net/auth/2.0"
    api_key: str
    identity: str = "http://specs.openid.net/auth/2.0/identifier_select"
    claimed_id: str = "http://specs.openid.net/auth/2.0/identifier_select"


class JWTConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.template"),
        env_nested_delimiter="__",
        env_prefix="JWT_",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openid: OpenIDConfig

    public: Path
    private: Path
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 5


class HTTPCORS(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.template"),
        env_prefix="HTTPCORS_",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    urls: List[str] = []


settingsjwt = JWTConfig()  # pyright: ignore
settingscors = HTTPCORS()  # pyright: ignore
