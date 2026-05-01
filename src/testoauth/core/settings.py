from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class OpenIDConfig(BaseModel):

    base_url: str
    api_key: str


class JWTConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.template"),
        env_nested_delimiter="__",
        env_prefix="JWT__",
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
