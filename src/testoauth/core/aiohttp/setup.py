import aiohttp
from contextlib import asynccontextmanager
from fastapi import FastAPI


class AiohttpSessionManager:
    """
    Менеджер сессий aiohttp.

    Создаёт одну сессию на всё приложение,
    переиспользует её и корректно закрывает при завершении.
    """

    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Получить текущую сессию.
        Вызывать только после startup (между startup и shutdown).
        """
        if self._session is None or self._session.closed:
            raise RuntimeError(
                "aiohttp session is not initialized. "
                "Make sure the application has started."
            )
        return self._session

    async def start(self) -> None:
        """Создать сессию. Вызывается при старте приложения."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def stop(self) -> None:
        """Закрыть сессию. Вызывается при остановке приложения."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None


aiohttp_session_manager = AiohttpSessionManager()


async def get_aiohttp_session() -> aiohttp.ClientSession:

    return aiohttp_session_manager.session
