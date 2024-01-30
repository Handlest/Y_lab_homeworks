import pytest
from starlette.testclient import TestClient

from config import Base, engine, get_test_db
from main import app
from utils import create_menu_json, create_submenu_json, create_dish_json


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    db = get_test_db()
    yield db
    db.close()


@pytest.fixture
def create_menu(client: TestClient):
    response = client.post(url="http://localhost:8000/api/v1/menus", json=create_menu_json())
    return response.json()['id']


@pytest.fixture
def create_submenu(create_menu, client: TestClient):
    response = client.post(url=f"http://localhost:8000/api/v1/menus/{create_menu}/submenus", json=create_submenu_json())
    return create_menu, response.json()['id']


@pytest.fixture
def create_dish(create_submenu, client: TestClient):
    menu_id = create_submenu[0]
    submenu_id = create_submenu[1]
    response = client.post(url=f"http://localhost:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=create_dish_json())
    return menu_id, submenu_id, response.json()['id']
