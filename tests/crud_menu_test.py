from utils import *


def test_menu_create(client):
    menu = create_menu_json()
    response = client.post('http://localhost/api/v1/menus', json=menu)
    assert response.status_code == 201


def test_menu_read(client):
    # Проверяем, что база данных пуста
    response = client.get('http://localhost/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []

    # Добавляем и считываем меню
    menu = create_menu_json()
    response = client.post('http://localhost/api/v1/menus', json=menu)
    menu_id = response.json()["id"]
    response2 = client.get(f'http://localhost/api/v1/menus/{menu_id}')
    assert response2.status_code == 200
    assert response2.json()["id"] == menu_id
    assert response2.json()['title'] == menu['title']
    assert response2.json()['description'] == menu['description']


def test_menu_update(client):
    # Проверяем, что база данных пуста
    response = client.get('http://localhost/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []

    # Создаём меню в базе данных
    menu = create_menu_json()
    response = client.post('http://localhost/api/v1/menus', json=menu)
    assert response.status_code == 201
    menu_id = response.json()["id"]
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()['title'] == menu['title']
    assert response.json()['description'] == menu['description']

    # Изменяем название меню
    response = client.patch(f'http://localhost/api/v1/menus/{menu_id}', json={"title": "new menu!"})
    assert response.status_code == 200
    assert response.json()['id'] == menu_id
    assert response.json()['title'] == "new menu!"
    assert response.json()['description'] == menu['description']


def test_menu_delete(client):
    # Проверяем, что база данных пуста
    response = client.get('http://localhost/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []

    # Создаём меню в базе данных
    menu = create_menu_json()
    response = client.post('http://localhost/api/v1/menus', json=menu)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Удаляем меню из базы данных и проверяем, что она действительно удалена
    response = client.delete(f'http://localhost/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}')
    assert response.status_code == 404
