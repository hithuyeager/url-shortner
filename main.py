from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import connect_to_db
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await connect_to_db()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
