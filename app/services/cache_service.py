import json
import time

from app.database import get_db


async def get_cached_weather(cache_key: str):
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT payload, expires_at FROM weather_cache WHERE cache_key = ?",
            (cache_key,),
        )
        row = await cursor.fetchone()

        if not row:
            return None

        if row["expires_at"] < int(time.time()):
            return None

        return json.loads(row["payload"])


async def save_weather_cache(cache_key: str, payload: dict, ttl: int = 600):
    expires_at = int(time.time()) + ttl

    async with get_db() as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO weather_cache (
                cache_key,
                payload,
                expires_at
            ) VALUES (?, ?, ?)
            """,
            (
                cache_key,
                json.dumps(payload),
                expires_at,
            ),
        )
        await db.commit()
