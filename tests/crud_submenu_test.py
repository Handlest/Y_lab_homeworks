from utils import *


def test_submenu_create(create_menu, client):
    response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=create_submenu_json())
    assert response.status_code == 201

def test_submenu_read(create_menu, client):
    # Проверили, что база данных пуста
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus')
    assert response.status_code == 200
    assert response.json() == []

    # Создали подменю
    submenu = create_submenu_json()
    response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
    submenu_id = response.json()["id"]

    # Проверили, что в базе данных успешно создалось нужное подменю
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()['title'] == submenu['title']
    assert response.json()['description'] == submenu['description']


def test_submenu_update(create_menu, client):
    # Проверяем, что база данных пуста
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus')
    assert response.status_code == 200
    assert response.json() == []

    # Создаём подменю в базе данных
    submenu = create_submenu_json()
    response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
    submenu_id = response.json()["id"]

    # Проверили, что в базе данных успешно создалось нужное подменю
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()['title'] == submenu['title']
    assert response.json()['description'] == submenu['description']

    # Изменяем название меню
    response = client.patch(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}',
                            json={"title": "new submenu!"})
    assert response.status_code == 200
    assert response.json()['id'] == submenu_id
    assert response.json()['title'] == "new submenu!"
    assert response.json()['description'] == submenu['description']


def test_submenu_delete(create_menu, client):
    # Проверяем, что база данных пуста
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus')
    assert response.status_code == 200
    assert response.json() == []

    # Создаём подменю в базе данных
    submenu = create_submenu_json()
    response = client.post(f'http://localhost/api/v1/menus/{create_menu}/submenus', json=submenu)
    submenu_id = response.json()["id"]

    # Проверили, что в базе данных успешно создалось нужное подменю
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()['title'] == submenu['title']
    assert response.json()['description'] == submenu['description']

    # Удаляем меню из базы данных и проверяем, что она действительно удалена
    response = client.delete(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
    assert response.status_code == 200
    response = client.get(f'http://localhost/api/v1/menus/{create_menu}/submenus/{submenu_id}')
    assert response.status_code == 404
