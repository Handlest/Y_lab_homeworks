import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models.models import Menu
from tests.conftest import async_session_maker
from utils import create_menu_json


def get_menu_url(endpoint=''):
    if endpoint != '':
        endpoint = '/' + endpoint
    return f'http://localhost/api/v1/menus{endpoint}'


class TestCrudMenus:
    @pytest.mark.asyncio
    async def test_menu_create(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu = create_menu_json()
            response = await ac.post(get_menu_url(), json=menu)
            assert response.status_code == 201

            # Проверяем что POST запрос возвращает правильные данные
            assert menu['title'] == response.json()['title']
            assert menu['description'] == response.json()['description']

            # Проверяем что данные в базе данных совпадают с возвращаемыми
            menu_entity = (await db.execute(select(Menu).where(Menu.id == response.json()['id']))).scalars().first()
            assert menu_entity.title == response.json()['title']
            assert menu_entity.description == response.json()['description']

    @pytest.mark.asyncio
    async def test_menu_read(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            # Проверяем, что база данных пуста
            response = await ac.get(get_menu_url())
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Menu))).first() is None

            # Добавляем информацию в базу данных
            menu = create_menu_json()
            response = await ac.post(get_menu_url(), json=menu)
            assert response.status_code == 201
            menu_id = response.json()['id']

            # Проверяем, что GET запрос возвращает правильные данные
            response2 = await ac.get(get_menu_url(menu_id))
            assert response2.status_code == 200
            menu_entity = (await db.execute(select(Menu).where(Menu.id == response2.json()['id']))).scalars().first()
            assert menu_entity.title == response2.json()['title']
            assert menu_entity.description == response2.json()['description']

    @pytest.mark.asyncio
    async def test_menu_update(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            # Проверяем, что база данных пуста
            response = await ac.get(get_menu_url())
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Menu))).first() is None

            # Создаём меню в базе данных
            menu = create_menu_json()
            response = await ac.post(get_menu_url(), json=menu)
            assert response.status_code == 201
            menu_id = response.json()['id']

            # Проверяем, что в базе данных создался первый вариант меню
            response = await ac.get(get_menu_url(menu_id))
            assert response.status_code == 200
            assert response.json()['id'] == menu_id
            assert response.json()['title'] == menu['title']
            assert response.json()['description'] == menu['description']
            assert (await db.execute(select(Menu))).first() is not None

            # Изменяем название меню и проверяем изменённое значение в базе данных
            response = await ac.patch(get_menu_url(menu_id), json={'title': 'new menu!'})
            assert response.status_code == 200
            assert response.json()['id'] == menu_id
            assert response.json()['title'] == 'new menu!'
            assert response.json()['description'] == menu['description']
            assert (await db.execute(select(Menu).where(Menu.title == 'new menu!'))).first() is not None

    @pytest.mark.asyncio
    async def test_menu_delete(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            # Проверяем, что база данных пуста
            response = await ac.get(get_menu_url())
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Menu))).first() is None

            # Создаём меню и проверяем его наличие в базе данных
            menu = create_menu_json()
            response = await ac.post(get_menu_url(), json=menu)
            assert response.status_code == 201
            menu_id = response.json()['id']
            assert (await db.get(Menu, menu_id)) is not None

            # Удаляем меню из базы данных и проверяем, что оно действительно удалено
            response = await ac.delete(get_menu_url(menu_id))
            assert response.status_code == 200
            response = await ac.get(get_menu_url(menu_id))
            assert response.status_code == 404
            assert (await db.execute(select(Menu))).first() is None
