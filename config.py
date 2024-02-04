import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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
    SQLALCHEMY_DATABASE_URL = (f'postgresql+asyncpg://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}'
                               f'@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_DATABASE}')
else:
    SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, enable_from_linting=False)
Base = declarative_base()
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


if os.getenv('TEST_MODE') == 'True':
    async def get_test_db():
        db = async_session()
        return db
