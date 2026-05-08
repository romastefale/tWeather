import aiosqlite

DB_PATH = 'data/weather.db'


async def set_cards_enabled(user_id: int, enabled: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS user_card_settings (
                user_id INTEGER PRIMARY KEY,
                enabled INTEGER NOT NULL
            )
            '''
        )

        await db.execute(
            '''
            INSERT OR REPLACE INTO user_card_settings (user_id, enabled)
            VALUES (?, ?)
            ''',
            (user_id, int(enabled)),
        )

        await db.commit()


async def are_cards_enabled(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS user_card_settings (
                user_id INTEGER PRIMARY KEY,
                enabled INTEGER NOT NULL
            )
            '''
        )

        cursor = await db.execute(
            'SELECT enabled FROM user_card_settings WHERE user_id = ?',
            (user_id,),
        )

        row = await cursor.fetchone()

        if not row:
            return True

        return bool(row[0])
