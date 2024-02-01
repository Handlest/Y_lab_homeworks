from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from models.models import Menu
from utils import create_menu_json


def get_menu_url(endpoint=''):
    if endpoint != '':
        endpoint = '/' + endpoint
    return f'http://localhost/api/v1/menus{endpoint}'


class TestCrudMenus:
    def test_menu_create(self, client: TestClient, db: Session):
        menu = create_menu_json()
        response = client.post(get_menu_url(), json=menu)
        assert response.status_code == 201

        # Проверяем что POST запрос возвращает правильные данные
        assert menu['title'] == response.json()['title']
        assert menu['description'] == response.json()['description']

        # Проверяем что данные в базе данных совпадают с возвращаемыми
        assert len(db.query(Menu).all()) == 1
        assert db.query(Menu).filter(Menu.id == response.json()['id']).first() is not None
        assert db.query(Menu).filter(Menu.title == response.json()['title']).first() is not None
        assert db.query(Menu).filter(Menu.description == response.json()['description']).first() is not None

    def test_menu_read(self, client: TestClient, db: Session):
        # Проверяем, что база данных пуста
        response = client.get(get_menu_url())
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Menu).all()) == 0

        # Добавляем информацию в базу данных
        menu = create_menu_json()
        response = client.post(get_menu_url(), json=menu)
        assert response.status_code == 201
        menu_id = response.json()['id']
        assert len(db.query(Menu).all()) == 1

        # Проверяем, что GET запрос возвращает правильные данные
        response2 = client.get(get_menu_url(menu_id))
        assert response2.status_code == 200
        assert response2.json()['id'] == response.json()['id'] == menu_id
        assert response2.json()['title'] == response.json()['title'] == menu['title']
        assert response2.json()['description'] == response.json()['description'] == menu['description']

    def test_menu_update(self, client: TestClient, db: Session):
        # Проверяем, что база данных пуста
        response = client.get(get_menu_url())
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Menu).all()) == 0

        # Создаём меню в базе данных
        menu = create_menu_json()
        response = client.post(get_menu_url(), json=menu)
        assert response.status_code == 201
        menu_id = response.json()['id']

        # Проверяем, что в базе данных создался первый вариант меню
        response = client.get(get_menu_url(menu_id))
        assert response.status_code == 200
        assert response.json()['id'] == menu_id
        assert response.json()['title'] == menu['title']
        assert response.json()['description'] == menu['description']
        assert len(db.query(Menu).all()) == 1
        assert db.query(Menu).filter(Menu.title == menu['title']).first() is not None

        # Изменяем название меню и проверяем изменённое значение в базе данных
        response = client.patch(get_menu_url(menu_id), json={'title': 'new menu!'})
        assert response.status_code == 200
        assert response.json()['id'] == menu_id
        assert response.json()['title'] == 'new menu!'
        assert response.json()['description'] == menu['description']
        assert len(db.query(Menu).all()) == 1
        assert db.query(Menu).filter(Menu.title == 'new menu!').first() is not None

    def test_menu_delete(self, client: TestClient, db: Session):
        # Проверяем, что база данных пуста
        response = client.get(get_menu_url())
        assert response.status_code == 200
        assert response.json() == []
        assert len(db.query(Menu).all()) == 0

        # Создаём меню и проверяем его наличие в базе данных
        menu = create_menu_json()
        response = client.post(get_menu_url(), json=menu)
        assert response.status_code == 201
        menu_id = response.json()['id']
        assert len(db.query(Menu).all()) == 1
        assert db.query(Menu).filter(Menu.id == menu_id).first() is not None

        # Удаляем меню из базы данных и проверяем, что оно действительно удалено
        response = client.delete(get_menu_url(menu_id))
        assert response.status_code == 200
        response = client.get(get_menu_url(menu_id))
        assert response.status_code == 404
        assert len(db.query(Menu).all()) == 0
