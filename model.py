import json

from conf import BASE_DIR


USERS = []
PROBLEMS = []
LAST_CALL = 0


def set_users(users):
    global USERS
    USERS = users


def get_users():
    global USERS
    return USERS[:]


def get_users_count():
    global USERS
    return len(USERS)


def get_problems():
    global PROBLEMS
    return PROBLEMS[:]


def set_problems(problems):
    global PROBLEMS
    PROBLEMS = problems


def save_problems():
    global PROBLEMS
    with open(BASE_DIR / "static" / "problems.json", "w", encoding="utf-8") as f:
        json.dump(PROBLEMS, f, indent=2)
    with open(BASE_DIR / "static" / "problems.txt", "w", encoding="utf-8") as f:
        json.dump(PROBLEMS, f, indent=2)
