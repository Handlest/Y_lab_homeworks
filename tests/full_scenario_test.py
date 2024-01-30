import pytest
from starlette.testclient import TestClient

from conftest import client, db
from main import app
from utils import *


class TestFullScenario:
    menu_id = int
    submenu_id = int
    first_dish_id = int
    second_dish_id = int
    client = TestClient(app)

    def test_create_menu(self, db):
        menu = create_menu_json()
        response = self.client.post('http://localhost/api/v1/menus', json=menu)
        assert response.status_code == 201

        # Проверяем что POST запрос возвращает правильные данные
        assert menu['title'] == response.json()['title']
        assert menu['description'] == response.json()['description']
        self.__class__.menu_id = response.json()["id"]

        # Проверяем что данные в базе данных совпадают с возвращаемыми
        assert len(db.query(Menu).all()) == 1
        assert db.query(Menu).filter(Menu.id == response.json()['id']).first() is not None
        assert db.query(Menu).filter(Menu.title == response.json()['title']).first() is not None
        assert db.query(Menu).filter(Menu.description == response.json()['description']).first() is not None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_create_submenu(self, db):
        submenu = create_submenu_json()
        response = self.client.post(f'http://localhost/api/v1/menus/{self.menu_id}/submenus', json=submenu)
        assert response.status_code == 201
        self.__class__.submenu_id = response.json()["id"]

        # Проверяем что POST запрос возвращает правильные данные
        assert submenu['title'] == response.json()['title']
        assert submenu['description'] == response.json()['description']

        # Проверяем что данные в базе данных совпадают с возвращаемыми
        assert len(db.query(Submenu).all()) == 1
        assert db.query(Submenu).filter(Submenu.id == response.json()['id']).first() is not None
        assert db.query(Submenu).filter(Submenu.title == response.json()['title']).first() is not None
        assert db.query(Submenu).filter(Submenu.description == response.json()['description']).first() is not None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_create_first_dish(self, client, db):
        dish = create_dish_json()
        response = client.post(f'http://localhost/api/v1/menus/'
                                       f'{self.menu_id}/submenus/'
                                       f'{self.submenu_id}/dishes', json=dish)
        assert response.status_code == 201
        self.first_dish_id = response.json()["id"]

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

    @pytest.mark.parametrize("prepare_database", [False])
    def test_create_second_dish(self, client, db):
        dish = create_dish_json(2)
        response = client.post(f'http://localhost/api/v1/menus/'
                                       f'{self.menu_id}/submenus/'
                                       f'{self.submenu_id}/dishes', json=dish)
        assert response.status_code == 201

        self.second_dish_id = response.json()["id"]

        # Проверяем что POST запрос возвращает правильные данные
        assert dish['title'] == response.json()['title']
        assert dish['description'] == response.json()['description']
        assert dish['price'] == response.json()['price']

        # Проверяем что данные в базе данных совпадают с возвращаемыми
        assert len(db.query(Dish).all()) == 2
        assert db.query(Dish).filter(Dish.id == response.json()['id']).first() is not None
        assert db.query(Dish).filter(Dish.title == response.json()['title']).first() is not None
        assert db.query(Dish).filter(Dish.description == response.json()['description']).first() is not None
        assert db.query(Dish).filter(Dish.price == response.json()['price']).first() is not None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_check_menu_counters(self, client, db):
        response = client.get(f'http://localhost/api/v1/menus/{self.menu_id}')
        assert response.json()["submenus_count"] == 1
        assert response.json()["dishes_count"] == 2
        assert db.query(Menu).filter(Menu.id == response.json()['id']).first() is not None
        assert db.query(Menu).filter(Menu.title == response.json()['title']).first() is not None
        assert db.query(Menu).filter(Menu.description == response.json()['description']).first() is not None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_check_submenu_counter(self, client, db):
        response = client.get(f'http://localhost/api/v1/menus/{self.menu_id}'
                                   f'/submenus/{self.submenu_id}')
        assert response.json()["dishes_count"] == 2
        assert db.query(Submenu).filter(Submenu.id == response.json()['id']).first() is not None
        assert db.query(Submenu).filter(Submenu.title == response.json()['title']).first() is not None
        assert db.query(Submenu).filter(Submenu.description == response.json()['description']).first() is not None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_delete_submenu(self, client, db):
        delete_submenu = client.delete(f'http://localhost/api/v1/menus/{self.menu_id}'
                                   f'/submenus/{self.submenu_id}')
        assert delete_submenu.status_code == 200
        assert db.query(Submenu).filter(Submenu.id == self.submenu_id).first() is None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_check_submenu_exists(self, client, db):
        check_submenus = client.get(f'http://localhost/api/v1/menus/{self.menu_id}'
                                   f'/submenus')
        assert check_submenus.status_code == 200
        assert check_submenus.json() == []
        assert len(db.query(Submenu).all()) == 0

    @pytest.mark.parametrize("prepare_database", [False])
    def test_check_dishes_exists(self, client, db):
        check_dishes = client.get(f'http://localhost/api/v1/menus/{self.menu_id}'
                                    f'/submenus/{self.submenu_id}/dishes')
        assert check_dishes.status_code == 200
        assert check_dishes.json() == []
        assert len(db.query(Dish).all()) == 0

    @pytest.mark.parametrize("prepare_database", [False])
    def test_check_menu_after_delete(self, client, db):
        check_menu = client.get(f'http://localhost/api/v1/menus/{self.menu_id}')
        assert check_menu.json()["submenus_count"] == 0
        assert check_menu.json()["dishes_count"] == 0
        assert db.query(Submenu).filter(Submenu.menu_id == self.menu_id).first() is None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_delete_menu(self, client, db):
        delete_menu = client.delete(f'http://localhost/api/v1/menus/{self.menu_id}')
        assert delete_menu.status_code == 200
        assert db.query(Menu).filter(Menu.id == self.menu_id).first() is None

    @pytest.mark.parametrize("prepare_database", [False])
    def test_check_menu_exists(self, client, db):
        check_menus = client.get(f'http://localhost/api/v1/menus/')
        assert check_menus.status_code == 200
        assert check_menus.json() == []
        assert len(db.query(Menu).all()) == 0