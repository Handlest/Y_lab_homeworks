# test_main.py

import json

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from config import Base, get_db

TEST_DB_URL = "postgresql://test_user_test:test_password_test@localhost:5433/test_db"

# Фикстура для создания и подключения к тестовой базе данных
@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()

# Фикстура для запуска приложения в тестовом режиме
@pytest.fixture
def test_app(monkeypatch, test_db):
    # Переопределение конфигурации для тестов
    monkeypatch.setenv("TEST_MODE", "True")
    app.dependency_map[get_db] = lambda: test_db
    yield TestClient(app)
    # Завершение транзакции и очистка данных после теста
    test_db.rollback()
    Base.metadata.drop_all(bind=test_db.bind)

# Тест для создания пользователя
def test_create_user(test_app, test_db):
    user_data = {"username": "testuser", "email": "testuser@example.com"}
    response = test_app.post("/users/", data=json.dumps(user_data))

    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]

# Тест для получения списка пользователей
def test_read_users(test_app):
    response = test_app.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
