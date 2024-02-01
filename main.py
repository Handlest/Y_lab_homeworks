from fastapi import FastAPI

from config import Base, engine
from routers.dish_routes import dish_router
from routers.menu_routes import menu_router
from routers.submenu_routes import submenu_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
