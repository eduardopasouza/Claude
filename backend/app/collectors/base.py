import logging
import httpx
import json
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from app.config import settings

logger = logging.getLogger("agrojus.collectors")


class BaseCollector:
    """Base class for all data collectors with caching support."""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.cache_dir = Path(settings.cache_dir) / source_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = settings.cache_ttl

    def _cache_key(self, query: str) -> str:
        return hashlib.sha256(query.encode()).hexdigest()

    def _get_cached(self, query: str) -> Optional[dict]:
        key = self._cache_key(query)
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        with open(cache_file, "r") as f:
            cached = json.load(f)

        expires_at = datetime.fromisoformat(cached["expires_at"])
        if datetime.now(timezone.utc) > expires_at:
            cache_file.unlink()
            return None

        return cached["data"]

    def _set_cached(self, query: str, data: dict) -> None:
        key = self._cache_key(query)
        cache_file = self.cache_dir / f"{key}.json"

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.cache_ttl)
        cached = {
            "data": data,
            "expires_at": expires_at.isoformat(),
            "source": self.source_name,
            "query": query,
        }

        with open(cache_file, "w") as f:
            json.dump(cached, f, ensure_ascii=False, default=str)

    async def _http_get(self, url: str, params: dict = None, headers: dict = None, timeout: float = 30.0) -> httpx.Response:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
