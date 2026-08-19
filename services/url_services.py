import secrets
import string
import asyncpg

from repositories.url_repository import get_original_url,store_url
from schemas.url import URLNotFoundError

MAX_RETRIES = 10

def gen_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))

async def create_short_url(conn, original_url):
    for _ in range(MAX_RETRIES):
        short_code = gen_random_string()

        try:
            data = await store_url(
                conn,
                short_code,
                original_url
            )
            return data["short_code"]

        except asyncpg.UniqueViolationError:
            continue

    raise RuntimeError("Failed to generate a unique short code")


async def navigate_to_original(
        conn: asyncpg.Connection,
        short_code: str
):
    original_url = await get_original_url(conn,short_code)
    if original_url is not None:
        return original_url
    raise URLNotFoundError()

    
