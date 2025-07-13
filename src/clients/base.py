from dataclasses import dataclass

from httpx import URL, AsyncClient


__all__ = ["BaseClient"]


@dataclass
class BaseClient:
    url: URL

    def __init__(self, client: AsyncClient) -> None:
        self.client = client
