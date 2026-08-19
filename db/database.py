from config import settings
import asyncpg

async def connect_to_db():
    return await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=5,
        max_size=20,
        command_timeout = 60
    )