import asyncpg

async def store_url(
        conn: asyncpg.Connection,
        short_code: str,
        original_url: str
):
    return await conn.fetchrow(
        """INSERT INTO urls (short_code,original_url) 
           values ($1,$2) RETURNING id,short_code,original_url,
           created_at
        """,short_code,original_url
    )

async def get_original_url(
        conn: asyncpg.Connection,
        short_code: str
):
    return await conn.fetchval(
        """SELECT original_url FROM urls WHERE 
           short_code = $1
        """,short_code
    )