from utils import create_dish_json


def test_dish_create(create_submenu, client):
    menu_id = create_submenu[0]
    submenu_id = create_submenu[1]
    response = client.post(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
                           json=create_dish_json(1))
    assert response.status_code == 201


def test_menu_read(create_submenu, client):
    # Проверили, что база данных пуста
    menu_id = create_submenu[0]
    submenu_id = create_submenu[1]
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []

    # Создали блюдо
    dish = create_dish_json(1)
    response = client.post(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
    dish_id = response.json()["id"]

    # Проверили, что в базе данных успешно создалось нужное блюдо
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()["id"] == dish_id
    assert response.json()['title'] == dish['title']
    assert response.json()['description'] == dish['description']
    assert response.json()['price'] == dish['price']


def test_menu_update(create_submenu, client):
    # Проверили, что база данных пуста
    menu_id = create_submenu[0]
    submenu_id = create_submenu[1]
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []

    # Создали блюдо
    dish = create_dish_json(1)
    response = client.post(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
    dish_id = response.json()["id"]

    # Проверили, что в базе данных успешно создалось нужное блюдо
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()["id"] == dish_id
    assert response.json()['title'] == dish['title']
    assert response.json()['description'] == dish['description']
    assert response.json()['price'] == dish['price']

    # Изменяем название блюда
    response = client.patch(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                            json={"title": "new dish!"})
    assert response.status_code == 200
    assert response.json()['id'] == dish_id
    assert response.json()['title'] == "new dish!"
    assert response.json()['description'] == dish['description']
    assert response.json()['price'] == dish['price']


def test_menu_delete(create_submenu, client):
    # Проверили, что база данных пуста
    menu_id = create_submenu[0]
    submenu_id = create_submenu[1]
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []

    # Создали блюдо
    dish = create_dish_json(1)
    response = client.post(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
    dish_id = response.json()["id"]

    # Проверили, что в базе данных успешно создалось нужное блюдо
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()["id"] == dish_id
    assert response.json()['title'] == dish['title']
    assert response.json()['description'] == dish['description']
    assert response.json()['price'] == dish['price']

    # Удаляем меню из базы данных и проверяем, что она действительно удалена
    response = client.delete(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    response = client.get(f'http://localhost/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 404
