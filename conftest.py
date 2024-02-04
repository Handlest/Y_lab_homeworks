# import pytest
# import pytest_asyncio
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.util import asyncio
# from starlette.testclient import TestClient
#
# from config import Base, engine, get_test_db
# from main import app
# from models.models import Dish, Menu, Submenu
# from utils import create_dish_json, create_menu_json, create_submenu_json
#
#
# @pytest_asyncio.fixture(scope='session')
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest_asyncio.fixture()
# async def client() -> AsyncClient:  # type: ignore
#     async with AsyncClient(app=app, base_url=URL) as client:
#         yield client
#         await client.aclose()
#
# @pytest.fixture(autouse=True)
# async def prepare_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#
# @pytest.fixture
# def client():
#     return TestClient(app)
#
#
# @pytest.fixture
# def db():
#     db = get_test_db()
#     yield db
#     db.close()
#
# # Затестить
# @pytest.fixture
# async def create_menu(client: TestClient, db: AsyncSession):
#     menu = create_menu_json()
#     db.add(Menu(**menu))
#     await db.commit()
#     return menu['id']
#
#
# @pytest.fixture
# async def create_submenu(create_menu, client: TestClient, db: AsyncSession):
#     menu = create_menu_json()
#     db.add(Menu(**menu))
#     await db.commit()
#     menu_id = menu['id']
#     submenu = create_submenu_json()
#     submenu['menu_id'] = menu_id
#     db.add(Submenu(**submenu))
#     await db.commit()
#     submenu_id = submenu['id']
#     return menu_id, submenu_id
#
#
# @pytest.fixture
# async def create_dish(create_submenu, client: TestClient, db: AsyncSession):
#     menu = create_menu_json()
#     db.add(Menu(**menu))
#     await db.commit()
#     menu_id = menu['id']
#     submenu = create_submenu_json()
#     submenu['menu_id'] = menu_id
#     db.add(Submenu(**submenu))
#     await db.commit()
#     submenu_id = submenu['id']
#     dish = create_dish_json()
#     dish['submenu_id'] = submenu_id
#     db.add(Dish(**dish))
#     await db.commit()
#     dish_id = dish['id']
#     return menu_id, submenu_id, dish_id
