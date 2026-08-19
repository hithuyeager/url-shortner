from fastapi import FastAPI
from contextlib import contextmanager

from db.database import connect_to_db
from api.routes import router

@contextmanager
async def lifespan(app: FastAPI):
    app.state.pool = connect_to_db()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)
