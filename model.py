import json

from conf import BASE_DIR


class Problem:
    problems = []

    def get_problems(self):
        return self.problems[:]

    def set_problems(self, prob):
        self.problems = prob

    def save_problems(self):
        with open(BASE_DIR / "static" / "problems.json", "w", encoding="utf-8") as f:
            json.dump(self.problems, f, indent=2)
        with open(BASE_DIR / "static" / "problems.txt", "w", encoding="utf-8") as f:
            json.dump(self.problems, f, indent=2)


class Users:
    users = []
    last_call = 0
    user_count = 0

    def set_users(self, users):
        self.users = users
        self.user_count = len(users)

    def get_users(self):
        return self.users[:]

    def get_users_count(self):
        return self.user_count


problem_obj = Problem()
users_obj = Users()
