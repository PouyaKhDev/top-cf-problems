import asyncio

from . import model
from . import view
from .model import users_obj, problems_obj

from .utils import get_int


def main():
    base_menu = model.Menu()
    base_menu.set_menu_options(
        ["Get top problems", "Get top problems from custom handles", "Settings"]
    )

    view.show_menu(base_menu.get_menu(), True)

    mi = 1
    ma = base_menu.get_menu_option_count()
    choice = None
    while choice == None:
        choice = get_int(mi, ma)
    if choice == -1:
        return

    match choice:
        case -1:
            return
        case 1:
            users_obj.fetch_users()
            asyncio.run(problems_obj.fetch(users_obj.get_users()))
            problems_obj.process()
            problems_obj.uniquify()
            problems_obj.save()
        case 2:
            pass
        case 3:
            pass
