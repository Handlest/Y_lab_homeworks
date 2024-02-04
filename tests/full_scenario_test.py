from httpx import AsyncClient
from sqlalchemy import select

from models.models import Dish, Menu, Submenu
from tests.conftest import async_session_maker
from utils import create_dish_json, create_menu_json, create_submenu_json


class TestFullScenario:
    menu_id = int
    submenu_id = int

    async def test_create_menu(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu = create_menu_json()
            response = await ac.post('http://localhost/api/v1/menus', json=menu)
            assert response.status_code == 201

            # Проверяем что POST запрос возвращает правильные данные
            assert menu['title'] == response.json()['title']
            assert menu['description'] == response.json()['description']
            self.__class__.menu_id = response.json()['id']

            # Проверяем что данные в базе данных совпадают с возвращаемыми
            menu_entity = (await db.execute(select(Menu).where(Menu.id == response.json()['id']))).scalars().first()
            assert menu_entity.title == response.json()['title']
            assert menu_entity.description == response.json()['description']

    async def test_create_submenu(self, ac: AsyncClient):
        async with async_session_maker() as db:
            submenu = create_submenu_json()
            response = await ac.post(f'http://localhost/api/v1/menus/{self.menu_id}/submenus', json=submenu)
            assert response.status_code == 201
            self.__class__.submenu_id = response.json()['id']

            # Проверяем что POST запрос возвращает правильные данные
            assert submenu['title'] == response.json()['title']
            assert submenu['description'] == response.json()['description']

            # Проверяем что данные в базе данных совпадают с возвращаемыми
            submenu_entity = (
                await db.execute(select(Submenu).where(Submenu.id == response.json()['id']))).scalars().first()
            assert submenu_entity.title == response.json()['title']
            assert submenu_entity.description == response.json()['description']

    async def test_create_first_dish(self, ac: AsyncClient):
        async with async_session_maker() as db:
            dish = create_dish_json()
            response = await ac.post(f'http://localhost/api/v1/menus/'
                                     f'{self.menu_id}/submenus/'
                                     f'{self.submenu_id}/dishes', json=dish)
            assert response.status_code == 201

            # Проверяем что POST запрос возвращает правильные данные
            assert dish['title'] == response.json()['title']
            assert dish['description'] == response.json()['description']
            assert dish['price'] == response.json()['price']

            # Проверяем что данные в базе данных совпадают с возвращаемыми
            dish_entity = (await db.execute(select(Dish).where(Dish.id == response.json()['id']))).scalars().first()
            assert dish_entity.title == response.json()['title']
            assert dish_entity.description == response.json()['description']
            assert dish_entity.price == response.json()['price']

    async def test_create_second_dish(self, ac: AsyncClient):
        async with async_session_maker() as db:
            dish = create_dish_json(2)
            response = await ac.post(f'http://localhost/api/v1/menus/'
                                     f'{self.menu_id}/submenus/'
                                     f'{self.submenu_id}/dishes', json=dish)
            assert response.status_code == 201

            # Проверяем что POST запрос возвращает правильные данные
            assert dish['title'] == response.json()['title']
            assert dish['description'] == response.json()['description']
            assert dish['price'] == response.json()['price']

            # Проверяем что данные в базе данных совпадают с возвращаемыми
            dish_entity = (await db.execute(select(Dish).where(Dish.id == response.json()['id']))).scalars().first()
            assert dish_entity.title == response.json()['title']
            assert dish_entity.description == response.json()['description']
            assert dish_entity.price == response.json()['price']

    async def test_check_menu_counters(self, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f'http://localhost/api/v1/menus/{self.menu_id}')
            assert response.json()['submenus_count'] == 1
            assert response.json()['dishes_count'] == 2
            menu_entity = (await db.execute(select(Menu).where(Menu.id == self.menu_id))).scalars().first()
            assert menu_entity.title == response.json()['title']
            assert menu_entity.description == response.json()['description']

    async def test_check_submenu_counter(self, ac: AsyncClient):
        async with async_session_maker() as db:
            response = await ac.get(f'http://localhost/api/v1/menus/{self.menu_id}'
                                    f'/submenus/{self.submenu_id}')
            assert response.json()['dishes_count'] == 2
            submenu_entity = (await db.execute(select(Submenu).where(Submenu.id == self.submenu_id))).scalars().first()
            assert submenu_entity.title == response.json()['title']
            assert submenu_entity.description == response.json()['description']

    async def test_delete_submenu(self, ac: AsyncClient):
        async with async_session_maker() as db:
            delete_submenu = await ac.delete(f'http://localhost/api/v1/menus/{self.menu_id}'
                                             f'/submenus/{self.submenu_id}')
            assert delete_submenu.status_code == 200
            assert (await db.execute(select(Submenu).where(Submenu.id == self.submenu_id))).scalars().first() is None

    async def test_check_submenu_exists(self, ac: AsyncClient):
        async with async_session_maker() as db:
            check_submenus = await ac.get(f'http://localhost/api/v1/menus/{self.menu_id}'
                                          f'/submenus')
            assert check_submenus.status_code == 200
            assert check_submenus.json() == []
            assert (await db.execute(select(Submenu))).scalars().first() is None

    async def test_check_dishes_exists(self, ac: AsyncClient):
        async with async_session_maker() as db:
            check_dishes = await ac.get(f'http://localhost/api/v1/menus/{self.menu_id}'
                                        f'/submenus/{self.submenu_id}/dishes')
            assert check_dishes.status_code == 200
            assert check_dishes.json() == []
            assert (await db.execute(select(Dish))).scalars().all() == []

    async def test_check_menu_after_delete(self, ac: AsyncClient):
        async with async_session_maker() as db:
            check_menu = await ac.get(f'http://localhost/api/v1/menus/{self.menu_id}')
            assert check_menu.json()['submenus_count'] == 0
            assert check_menu.json()['dishes_count'] == 0
            assert (await db.execute(select(Submenu).where(Submenu.menu_id == self.menu_id))).scalars().first() is None

    async def test_delete_menu(self, ac: AsyncClient):
        async with async_session_maker() as db:
            delete_menu = await ac.delete(f'http://localhost/api/v1/menus/{self.menu_id}')
            assert delete_menu.status_code == 200
            assert (await db.execute(select(Menu))).scalars().first() is None

    async def test_check_menu_exists(self, ac: AsyncClient):
        async with async_session_maker() as db:
            check_menus = await ac.get('http://localhost/api/v1/menus')
            assert check_menus.status_code == 200
            assert check_menus.json() == []
            assert (await db.execute(select(Menu))).scalars().all() == []
