import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()


if os.getenv("TEST_MODE") == "True":
    SQLALCHEMY_DATABASE_URL = (f'postgresql://{os.getenv("TEST_DB_USERNAME")}:'
                               f'{os.getenv("TEST_DB_PASSWORD")}@{os.getenv("TEST_DB_HOST")}:'
                               f'{os.getenv("TEST_DB_PORT")}/{os.getenv("TEST_DB_DATABASE")}')
else:
    SQLALCHEMY_DATABASE_URL = (f'postgresql://{os.getenv("DB_USERNAME")}:'
                               f'{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:'
                               f'{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}')


engine = create_engine(SQLALCHEMY_DATABASE_URL, enable_from_linting=False)
Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
