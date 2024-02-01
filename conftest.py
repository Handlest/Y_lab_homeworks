import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from config import Base, engine, get_test_db
from main import app
from models.models import Dish, Menu, Submenu
from utils import create_dish_json, create_menu_json, create_submenu_json


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
def create_menu(client: TestClient, db: Session):
    menu = create_menu_json()
    db.add(Menu(**menu))
    db.commit()
    menu_id = db.query(Menu).filter(Menu.title == menu['title']).first().id
    return menu_id


@pytest.fixture
def create_submenu(create_menu, client: TestClient, db: Session):
    menu = create_menu_json()
    db.add(Menu(**menu))
    db.commit()
    menu_id = db.query(Menu).filter(Menu.title == menu['title']).first().id
    submenu = create_submenu_json()
    submenu['menu_id'] = menu_id
    db.add(Submenu(**submenu))
    db.commit()
    submenu_id = db.query(Submenu).filter(Submenu.title == submenu['title']).first().id
    return menu_id, submenu_id


@pytest.fixture
def create_dish(create_submenu, client: TestClient, db: Session):
    menu = create_menu_json()
    db.add(Menu(**menu))
    db.commit()
    menu_id = db.query(Menu).filter(Menu.title == menu['title']).first().id
    submenu = create_submenu_json()
    submenu['menu_id'] = menu_id
    db.add(Submenu(**submenu))
    db.commit()
    submenu_id = db.query(Submenu).filter(Submenu.title == submenu['title']).first().id
    dish = create_dish_json()
    dish['submenu_id'] = submenu_id
    db.add(Dish(**dish))
    db.commit()
    dish_id = db.query(Dish).filter(Dish.title == dish['title']).first().id
    return menu_id, submenu_id, dish_id
