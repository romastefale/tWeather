import time

from app.database import get_db



def normalize_location_text(value: str | None):
    if value is None:
        return None

    return " ".join(str(value).strip().split())


async def save_user_location(
    user_id: int,
    name: str,
    latitude: float,
    longitude: float,
    country: str | None = None,
    admin1: str | None = None,
) -> None:
    name = normalize_location_text(name)
    country = normalize_location_text(country)
    admin1 = normalize_location_text(admin1)

    async with get_db() as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO user_locations (
                user_id,
                name,
                country,
                admin1,
                latitude,
                longitude,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                name,
                country,
                admin1,
                latitude,
                longitude,
                int(time.time()),
            ),
        )
        await db.commit()


async def get_user_location(user_id: int):
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT * FROM user_locations WHERE user_id = ?",
            (user_id,),
        )
        return await cursor.fetchone()
