from repository.repository import DishRepository, MenuRepository, SubmenuRepository
from services.dish_service import DishService
from services.menu_service import MenuService
from services.submenu_service import SubmenuService


def menu_service():
    return MenuService(MenuRepository)


def submenu_service():
    return SubmenuService(SubmenuRepository)


def dish_service():
    return DishService(DishRepository)
