import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')

TEST_DB_USERNAME = os.getenv('TEST_DB_USERNAME')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
TEST_DB_HOST = os.getenv('TEST_DB_HOST')
TEST_DB_PORT = os.getenv('TEST_DB_PORT')
TEST_DB_DATABASE = os.getenv('TEST_DB_DATABASE')

if os.getenv('TEST_MODE') == 'True':
    SQLALCHEMY_DATABASE_URL = (f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}'
                               f'@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_DATABASE}')
else:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'


engine = create_engine(SQLALCHEMY_DATABASE_URL, enable_from_linting=False)
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if os.getenv('TEST_MODE') == 'True':
    def get_test_db():
        db = SessionLocal()
        return db
