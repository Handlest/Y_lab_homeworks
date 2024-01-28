from utils import *


def test_full_scenario(client):
    menu = create_menu_json()
    menu_response = client.post('http://localhost/api/v1/menus', json=menu)
    assert menu_response.status_code == 201

    submenu = create_submenu_json()
    submenu_response = client.post(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}/submenus', json=submenu)
    assert submenu_response.status_code == 201

    dish1 = create_dish_json(1)
    dish1_response = client.post(f'http://localhost/api/v1/menus/'
                                   f'{menu_response.json()["id"]}/submenus/'
                                   f'{submenu_response.json()["id"]}/dishes', json=dish1)
    assert dish1_response.status_code == 201

    dish2 = create_dish_json(2)
    dish2_response = client.post(f'http://localhost/api/v1/menus/'
                                   f'{menu_response.json()["id"]}/submenus/'
                                   f'{submenu_response.json()["id"]}/dishes', json=dish2)
    assert dish2_response.status_code == 201

    check_menu = client.get(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}')
    assert check_menu.json()["submenus_count"] == 1
    assert check_menu.json()["dishes_count"] == 2

    check_submenu = client.get(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}'
                               f'/submenus/{submenu_response.json()["id"]}')
    assert check_submenu.json()["dishes_count"] == 2

    delete_submenu = client.delete(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}'
                               f'/submenus/{submenu_response.json()["id"]}')
    assert delete_submenu.status_code == 200

    check_submenus = client.get(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}'
                               f'/submenus')
    assert check_submenus.status_code == 200
    assert check_submenus.json() == []

    check_dishes = client.get(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}'
                                f'/submenus/{submenu_response.json()["id"]}/dishes')
    assert check_dishes.status_code == 200
    assert check_dishes.json() == []

    check_menu = client.get(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}')
    assert check_menu.json()["submenus_count"] == 0
    assert check_menu.json()["dishes_count"] == 0

    delete_menu = client.delete(f'http://localhost/api/v1/menus/{menu_response.json()["id"]}')
    assert delete_menu.status_code == 200

    check_menus = client.get(f'http://localhost/api/v1/menus/')
    assert check_menus.status_code == 200
    assert check_menus.json() == []