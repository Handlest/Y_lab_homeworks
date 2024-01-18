from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from config import Base, engine
from routers.menu_routes import user_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user_router)

