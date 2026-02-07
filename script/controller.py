import asyncio
import sys


import conf
from . import model
from . import view
from .model import users_obj, problems_obj
from .utils import get_int, get_custom_users


def main():
    base_menu = model.Menu()
    base_menu.set_menu_options(
        [
            "Get top problems by users and problems ratings",
            "Get top problems from custom handles",
            "Settings",
        ]
    )
    view.show_menu(base_menu.get_menu(), True)

    mi = 1
    ma = base_menu.get_menu_option_count()
    choice = None
    while choice == None:
        choice = get_int(mi, ma)

    match choice:
        case -1:
            sys.exit(0)
        case 1:
            users_obj.fetch_users()
        case 2:
            print(
                "For adding custom users, open custom_user.txt file and add a comma-separated list of Codeforces handles. exp: tourist, Benq, ..."
            )
            print("you can also write handles on multiple lines.\n")

            choice2 = input("Press Enter to continue...")
            if choice2 == -1:
                sys.exit(0)

            users_obj.set_users(get_custom_users())

    asyncio.run(problems_obj.fetch(users_obj.get_users()))
    problems_obj.process()
    problems_obj.uniquify()
    problems_obj.save()
    problems_obj.print_top()
