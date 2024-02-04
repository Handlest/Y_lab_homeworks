from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.util import asyncio
from starlette.testclient import TestClient

from config import (
    TEST_DB_DATABASE,
    TEST_DB_HOST,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
    TEST_DB_USERNAME,
    Base,
)
from main import app
from models.models import Dish, Menu, Submenu
from utils import create_dish_json, create_menu_json, create_submenu_json

DATABASE_URL_TEST = f'postgresql+asyncpg://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_DATABASE}'
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        session.close()

# app.dependency_overrides[get_db()] = override_get_async_session


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def clear_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='function')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


client = TestClient(app)


@pytest.fixture
async def create_dish():
    async with async_session_maker() as db:
        menu = create_menu_json()
        db.add(Menu(**menu))
        await db.commit()
        menu_id = menu['id']
        submenu = create_submenu_json()
        submenu['menu_id'] = menu_id
        db.add(Submenu(**submenu))
        await db.commit()
        submenu_id = submenu['id']
        dish = create_dish_json()
        dish['submenu_id'] = submenu_id
        db.add(Dish(**dish))
        await db.commit()
        dish_id = dish['id']
        return menu_id, submenu_id, dish_id
