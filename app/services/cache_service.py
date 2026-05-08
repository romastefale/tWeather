import json
import time

from app.database import get_db

CACHE_CLEANUP_INTERVAL = 3600
LAST_CACHE_CLEANUP = 0


async def cleanup_expired_weather_cache(now: int):
    global LAST_CACHE_CLEANUP

    if now - LAST_CACHE_CLEANUP < CACHE_CLEANUP_INTERVAL:
        return

    async with get_db() as db:
        await db.execute(
            "DELETE FROM weather_cache WHERE expires_at < ?",
            (now,),
        )
        await db.commit()

    LAST_CACHE_CLEANUP = now


async def get_cached_weather(cache_key: str):
    now = int(time.time())

    await cleanup_expired_weather_cache(now)

    async with get_db() as db:
        cursor = await db.execute(
            "SELECT payload, expires_at FROM weather_cache WHERE cache_key = ?",
            (cache_key,),
        )
        row = await cursor.fetchone()

        if not row:
            return None

        if row["expires_at"] < now:
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
