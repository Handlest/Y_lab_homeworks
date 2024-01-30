from starlette.testclient import TestClient

from utils import *


def get_submenu_url(menu_id, endpoint=''):
    if endpoint != '':
        endpoint = "/" + endpoint
    return f"http://localhost/api/v1/menus{menu_id}/submenus{endpoint}"

class TestCrudSubmenus:

    def test_submenu_create(self, create_menu, client: TestClient, db: Session):
        submenu = create_submenu_json()
        response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
        assert response.status_code == 201

        # Проверяем что POST запрос возвращает правильные данные
        assert submenu['title'] == response.json()['title']
        assert submenu['description'] == response.json()['description']

        # Проверяем что данные в базе данных совпадают с возвращаемыми
        assert len(db.query(Submenu).all()) == 1
        assert db.query(Submenu).filter(Submenu.id == response.json()['id']).first() is not None
        assert db.query(Submenu).filter(Submenu.title == response.json()['title']).first() is not None
        assert db.query(Submenu).filter(Submenu.description == response.json()['description']).first() is not None

    def test_submenu_read(self, create_menu, client: TestClient, db: Session):
        # Проверяем, что база данных пуста
        response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus')
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Submenu).all()) == 0

        # Добавляем информацию в базу данных
        submenu = create_submenu_json()
        response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
        assert response.status_code == 201
        submenu_id = response.json()["id"]
        assert len(db.query(Submenu).all()) == 1

        # Проверяем, что GET запрос возвращает правильные данные
        response2 = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
        assert response2.status_code == 200
        assert response2.json()["id"] == response.json()["id"] == submenu_id
        assert response2.json()['title'] == response.json()['title'] == submenu['title']
        assert response2.json()['description'] == response.json()['description'] == submenu['description']


    def test_submenu_update(self, create_menu, client: TestClient, db: Session):
        # Проверяем, что база данных пуста
        response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus')
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Submenu).all()) == 0

        # Создаём подменю в базе данных
        submenu = create_submenu_json()
        response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
        assert response.status_code == 201
        submenu_id = response.json()["id"]

        # Проверяем, что в базе данных создался первый вариант подменю
        response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
        assert response.status_code == 200
        assert response.json()["id"] == submenu_id
        assert response.json()['title'] == submenu['title']
        assert response.json()['description'] == submenu['description']
        assert len(db.query(Submenu).all()) == 1
        assert db.query(Submenu).filter(Submenu.title == submenu['title']).first() is not None

        # Изменяем название подменю и проверяем изменённое значение в базе данных
        response = client.patch(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}',
                                json={"title": "new submenu!"})
        assert response.status_code == 200
        assert response.json()['id'] == submenu_id
        assert response.json()['title'] == "new submenu!"
        assert response.json()['description'] == submenu['description']
        assert len(db.query(Submenu).all()) == 1
        assert db.query(Submenu).filter(Submenu.title == "new submenu!").first() is not None


    def test_submenu_delete(self, create_menu, client: TestClient, db: Session):
        # Проверяем, что база данных пуста
        response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus')
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Submenu).all()) == 0

        # Создаём подменю и проверяем его наличие в базе данных
        submenu = create_submenu_json()
        response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
        assert response.status_code == 201
        submenu_id = response.json()["id"]
        assert len(db.query(Submenu).all()) == 1

        # Удаляем подменю из базы данных и проверяем, что оно действительно удалено
        response = client.delete(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
        assert response.status_code == 200
        response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
        assert response.status_code == 404
        assert len(db.query(Submenu).all()) == 0
