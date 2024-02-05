import os

import aioredis
from dotenv import load_dotenv
from fastapi import FastAPI

from routers.dish_routes import dish_router
from routers.menu_routes import menu_router
from routers.submenu_routes import submenu_router

app = FastAPI()

load_dotenv()

redis = None


@app.on_event('startup')
async def start_redis():
    global redis
    redis = await aioredis.from_url('redis://redis', db=1)


if not os.getenv('TEST_MODE'):
    from config import Base, engine

    @app.on_event('startup')
    async def init_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
