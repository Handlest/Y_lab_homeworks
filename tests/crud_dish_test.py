import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models.models import Dish
from tests.conftest import async_session_maker
from utils import create_dish_json, create_submenu, reverse


class TestCrudDishes:
    @pytest.mark.asyncio
    async def test_dish_create(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            menu_id, submenu_id = await create_submenu(db)
            dish = create_dish_json()
            response = await ac.post(reverse(route_name='post_dish', menu_id=menu_id, submenu_id=submenu_id), json=dish)
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

    @pytest.mark.asyncio
    async def test_dish_read(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            # Проверили, что база данных пуста
            menu_id, submenu_id = await create_submenu(db)
            response = await ac.get(reverse(route_name='get_dish_list', menu_id=menu_id, submenu_id=submenu_id))
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Dish))).first() is None

            # Добавляем информацию в базу данных
            dish = create_dish_json()
            response = await ac.post(reverse(route_name='post_dish', menu_id=menu_id, submenu_id=submenu_id), json=dish)
            assert response.status_code == 201
            dish_id = response.json()['id']
            assert (await db.execute(select(Dish))).first() is not None

            # Проверяем, что GET запрос возвращает правильные данные
            response = await ac.get(reverse(route_name='get_dish_by_id', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))
            assert response.status_code == 200
            assert response.json()['id'] == dish_id
            assert response.json()['title'] == dish['title']
            assert response.json()['description'] == dish['description']
            assert response.json()['price'] == dish['price']

    @pytest.mark.asyncio
    async def test_dish_update(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            # Проверили, что база данных пуста
            menu_id, submenu_id = await create_submenu(db)
            response = await ac.get(reverse(route_name='get_dish_list', menu_id=menu_id, submenu_id=submenu_id))
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Dish))).first() is None

            # Создали блюдо
            dish = create_dish_json()
            response = await ac.post(reverse(route_name='post_dish', menu_id=menu_id, submenu_id=submenu_id), json=dish)
            assert response.status_code == 201
            dish_id = response.json()['id']

            # Проверили, что в базе данных успешно создалось нужное блюдо
            response = await ac.get(reverse(route_name='get_dish_by_id', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))
            assert response.status_code == 200
            assert response.json()['id'] == dish_id
            assert response.json()['title'] == dish['title']
            assert response.json()['description'] == dish['description']
            assert response.json()['price'] == dish['price']
            assert (await db.execute(select(Dish).where(Dish.title == response.json()['title']))).first() is not None

            # Изменяем название блюда
            response = await ac.patch(reverse(route_name='patch_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id),
                                      json={'title': 'new dish!'})
            assert response.status_code == 200
            assert response.json()['id'] == dish_id
            assert response.json()['title'] == 'new dish!'
            assert response.json()['description'] == dish['description']
            assert response.json()['price'] == dish['price']
            assert (await db.execute(select(Dish).where(Dish.title == 'new dish!'))).first() is not None

    @pytest.mark.asyncio
    async def test_dish_delete(self, ac: AsyncClient, clear_database):
        async with async_session_maker() as db:
            # Проверили, что база данных пуста
            menu_id, submenu_id = await create_submenu(db)
            response = await ac.get(reverse(route_name='get_dish_list', menu_id=menu_id, submenu_id=submenu_id))
            assert response.status_code == 200
            assert response.json() == []
            assert (await db.execute(select(Dish))).first() is None

            # Создали блюдо
            dish = create_dish_json()
            response = await ac.post(reverse(route_name='post_dish', menu_id=menu_id, submenu_id=submenu_id), json=dish)
            assert response.status_code == 201
            dish_id = response.json()['id']
            assert (await db.execute(select(Dish))).first() is not None

            # Удаляем блюдо из базы данных и проверяем, что оно действительно удалено
            response = await ac.delete(reverse(route_name='delete_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))
            assert response.status_code == 200
            response = await ac.get(reverse(route_name='get_dish_by_id', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))
            assert response.status_code == 404
            assert (await db.execute(select(Dish))).first() is None
