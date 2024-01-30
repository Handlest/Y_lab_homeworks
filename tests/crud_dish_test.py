from starlette.testclient import TestClient

from utils import *


def get_dish_url(menu_id, submenu_id, endpoint=''):
    if endpoint != '':
        endpoint = "/" + endpoint
    return f"http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes{endpoint}"


class TestCrudMenus:
    def test_dish_create(self, create_submenu, client: TestClient, db: Session):
        menu_id, submenu_id = create_submenu
        dish = create_dish_json()
        response = client.post(get_dish_url(menu_id, submenu_id), json=dish)
        assert response.status_code == 201

        # Проверяем что POST запрос возвращает правильные данные
        assert dish['title'] == response.json()['title']
        assert dish['description'] == response.json()['description']
        assert dish['price'] == response.json()['price']

        # Проверяем что данные в базе данных совпадают с возвращаемыми
        assert len(db.query(Dish).all()) == 1
        assert db.query(Dish).filter(Dish.id == response.json()['id']).first() is not None
        assert db.query(Dish).filter(Dish.title == response.json()['title']).first() is not None
        assert db.query(Dish).filter(Dish.description == response.json()['description']).first() is not None
        assert db.query(Dish).filter(Dish.price == response.json()['price']).first() is not None

    def test_dish_read(self, create_submenu, client: TestClient, db: Session):
        # Проверили, что база данных пуста
        menu_id, submenu_id = create_submenu
        response = client.get(get_dish_url(menu_id, submenu_id))
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Dish).all()) == 0

        # Добавляем информацию в базу данных
        dish = create_dish_json()
        response = client.post(get_dish_url(menu_id, submenu_id), json=dish)
        assert response.status_code == 201
        dish_id = response.json()["id"]
        assert len(db.query(Dish).all()) == 1

        # Проверяем, что GET запрос возвращает правильные данные
        response = client.get(get_dish_url(menu_id, submenu_id, dish_id))
        assert response.status_code == 200
        assert response.json()["id"] == dish_id
        assert response.json()['title'] == dish['title']
        assert response.json()['description'] == dish['description']
        assert response.json()['price'] == dish['price']

    def test_dish_update(self, create_submenu, client: TestClient, db: Session):
        # Проверили, что база данных пуста
        menu_id, submenu_id = create_submenu
        response = client.get(get_dish_url(menu_id, submenu_id))
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Dish).all()) == 0

        # Создали блюдо
        dish = create_dish_json()
        response = client.post(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
        assert response.status_code == 201
        dish_id = response.json()["id"]

        # Проверили, что в базе данных успешно создалось нужное блюдо
        response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        assert response.status_code == 200
        assert response.json()["id"] == dish_id
        assert response.json()['title'] == dish['title']
        assert response.json()['description'] == dish['description']
        assert response.json()['price'] == dish['price']
        assert len(db.query(Dish).all()) == 1
        assert db.query(Dish).filter(Dish.title == dish['title']).first() is not None

        # Изменяем название блюда
        response = client.patch(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                                json={"title": "new dish!"})
        assert response.status_code == 200
        assert response.json()['id'] == dish_id
        assert response.json()['title'] == "new dish!"
        assert response.json()['description'] == dish['description']
        assert response.json()['price'] == dish['price']
        assert len(db.query(Dish).all()) == 1
        assert db.query(Dish).filter(Dish.title == "new dish!").first() is not None

    def test_dish_delete(self, create_submenu, client: TestClient, db: Session):
        # Проверили, что база данных пуста
        menu_id, submenu_id = create_submenu
        response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Dish).all()) == 0

        # Создали блюдо
        dish = create_dish_json()
        response = client.post(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
        assert response.status_code == 201
        dish_id = response.json()["id"]
        assert len(db.query(Dish).all()) == 1

        # Удаляем меню из базы данных и проверяем, что она действительно удалена
        response = client.delete(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        assert response.status_code == 200
        response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        assert response.status_code == 404
        assert len(db.query(Dish).all()) == 0
