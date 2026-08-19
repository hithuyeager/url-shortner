from fastapi import APIRouter,Request,Depends,HTTPException
import asyncpg
from fastapi.responses import RedirectResponse

from schemas.url import URLNotFoundError,URLCreate,URLResponse
from services.url_services import create_short_url,navigate_to_original
from config import settings

router = APIRouter()

async def get_pool(request: Request) -> asyncpg.pool:
    return request.app.state.pool

async def get_connection(pool = Depends(get_pool)):
    async with pool.acquire() as conn:
        yield conn

@router.post("/shorten",
            response_model=URLResponse,
            status_code=201)
async def shorten_url(
    data: URLCreate,
    conn: asyncpg.Connection = Depends(get_connection)
):
    short_code = await create_short_url(conn,data.original_url)

    return URLResponse(
        short_url=f"{settings.base_url}/{short_code}"
        )


@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    conn: asyncpg.Connection = Depends(get_connection)
):
    try:
        original_url = await navigate_to_original(conn,short_code)
    except URLNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="short code not found"
            )
    
    return RedirectResponse(
        url=original_url,
        status_code=307
    )
    
    
