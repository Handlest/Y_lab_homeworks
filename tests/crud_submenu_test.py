from httpx import AsyncClient
from sqlalchemy import select

from models.models import Submenu
from tests.conftest import async_session_maker
from utils import create_menu, create_submenu_json, reverse


class TestCrudSubmenus:
    async def test_submenu_create(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu_id = await create_menu(db)
            submenu = create_submenu_json()
            response = await ac.post(reverse(route_name='post_submenu', menu_id=menu_id), json=submenu)
            assert response.status_code == 201

            # Проверяем что POST запрос возвращает правильные данные
            assert submenu['title'] == response.json()['title']
            assert submenu['description'] == response.json()['description']

            # Проверяем что данные в базе данных совпадают с возвращаемыми
            submenu_entity = (await db.execute(select(Submenu).where(Submenu.id == response.json()['id']))).scalars().first()
            assert submenu_entity.title == response.json()['title']
            assert submenu_entity.description == response.json()['description']

    async def test_submenu_read(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu_id = await create_menu(db)
            # Проверяем, что база данных пуста
            response = await ac.get(reverse(route_name='get_submenu_list', menu_id=menu_id))
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Submenu))).first() is None

            # Добавляем информацию в базу данных
            submenu = create_submenu_json()
            response = await ac.post(reverse(route_name='post_submenu', menu_id=menu_id), json=submenu)
            assert response.status_code == 201
            submenu_id = response.json()['id']

            # Проверяем, что GET запрос возвращает правильные данные
            response2 = await ac.get(reverse(route_name='get_submenu_by_id', menu_id=menu_id, submenu_id=submenu_id))
            assert response2.status_code == 200
            submenu_entity = (await db.execute(select(Submenu).where(Submenu.id == response2.json()['id']))).scalars().first()
            assert submenu_entity.title == response2.json()['title']
            assert submenu_entity.description == response2.json()['description']

    async def test_submenu_update(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu_id = await create_menu(db)
            # Проверяем, что база данных пуста
            response = await ac.get(reverse(route_name='get_submenu_list', menu_id=menu_id))
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Submenu))).first() is None

            # Создаём подменю в базе данных
            submenu = create_submenu_json()
            response = await ac.post(reverse(route_name='post_submenu', menu_id=menu_id), json=submenu)
            assert response.status_code == 201
            submenu_id = response.json()['id']

            # Проверяем, что в базе данных создался первый вариант подменю
            response = await ac.get(reverse(route_name='get_submenu_by_id', menu_id=menu_id, submenu_id=submenu_id))
            assert response.status_code == 200
            assert response.json()['id'] == submenu_id
            assert response.json()['title'] == submenu['title']
            assert response.json()['description'] == submenu['description']
            assert (await db.execute(select(Submenu))).first() is not None

            # Изменяем название подменю и проверяем изменённое значение в базе данных
            response = await ac.patch(reverse(route_name='patch_submenu', menu_id=menu_id, submenu_id=submenu_id),
                                      json={'title': 'new submenu!'})
            assert response.status_code == 200
            assert response.json()['id'] == submenu_id
            assert response.json()['title'] == 'new submenu!'
            assert response.json()['description'] == submenu['description']
            assert (await db.execute(select(Submenu).where(Submenu.title == 'new submenu!'))).first() is not None

    async def test_submenu_delete(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu_id = await create_menu(db)
            # Проверяем, что база данных пуста
            response = await ac.get(reverse(route_name='get_submenu_list', menu_id=menu_id))
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Submenu))).first() is None

            # Создаём подменю и проверяем его наличие в базе данных
            submenu = create_submenu_json()
            response = await ac.post(reverse(route_name='post_submenu', menu_id=menu_id), json=submenu)
            assert response.status_code == 201
            submenu_id = response.json()['id']
            assert (await db.get(Submenu, submenu_id)) is not None

            # Удаляем подменю из базы данных и проверяем, что оно действительно удалено
            response = await ac.delete(reverse(route_name='delete_submenu', menu_id=menu_id, submenu_id=submenu_id))
            assert response.status_code == 200
            response = await ac.get(reverse(route_name='get_submenu_by_id', menu_id=menu_id, submenu_id=submenu_id))
            assert response.status_code == 404
            assert (await db.execute(select(Submenu))).first() is None
