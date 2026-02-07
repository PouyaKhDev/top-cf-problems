import json
import logging
import requests
import aiohttp


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


from .conf import (
    BASE_DIR,
    BASE_URL,
    USER_MIN_RATING,
    USER_MAX_RATING,
    ACTIVE_USERS,
    START_TIME_STAMPS,
    USER_COUNT,
    PROBLEM_COUNT,
    PROBLEM_MIN_RATING,
    PROBLEM_MAX_RATING,
)
from .utils import is_in_rating_range, fetch


class Problems:

    def __init__(self, *args, **kwargs):
        self.problems = []
        self.problems_url = f"{BASE_URL}/user.status"

    def get_problems(self):
        return self.problems[:]

    def set_problems(self, prob):
        self.problems = prob

    def save(self):
        logging.info(
            f"Maximum of {PROBLEM_COUNT} top problems (you can change it in settings), are being saved in 'problems.json' and 'problems.txt'"
        )

        if len(self.problems) > PROBLEM_COUNT:
            self.problems = self.problems[:PROBLEM_COUNT]

        with open(BASE_DIR / "problems.json", "w", encoding="utf-8") as f:
            json.dump(self.problems, f, indent=2)
        with open(BASE_DIR / "problems.txt", "w", encoding="utf-8") as f:
            json.dump(self.problems, f, indent=2)

        logging.info("Problems are saved successfully.")

    async def fetch(self, users):
        urls = [f"{self.problems_url}?handle={handle}" for handle in users]

        logging.info("Fetching problems...")
        results = []
        try:
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    data = await fetch(session, url)
                    results.extend(data["result"])

                    logging.info(
                        f"{len(data["result"])} problems are fetched from this handle: {url.split("=")[1]}"
                    )
        except aiohttp.ClientError as e:
            logging.info(f"Request failed: {e}")
        except Exception as e:
            logging.info(f"Something went wrong: {e}")
        else:
            self.problems = results
            logging.info("Problems are fetched successfully.")

    def process(self):
        logging.info("Processing problems...")

        prob = []
        for sub in self.problems:
            if (
                sub["verdict"] != "OK"
                or sub["creationTimeSeconds"] < START_TIME_STAMPS
                or "rating" not in sub["problem"]
                or sub["problem"]["rating"] < PROBLEM_MIN_RATING
                or sub["problem"]["rating"] > PROBLEM_MAX_RATING
            ):
                continue

            pr = {
                "contest_id": sub["contestId"],
                "index": sub["problem"]["index"],
                "rating": sub["problem"]["rating"],
                "id": f"{sub["problem"]["contestId"]}#{sub["problem"]["index"]}",
                "url": f"https://codeforces.com/contest/{sub["contestId"]}/problem/{sub["problem"]["index"]}",
            }

            prob.append(pr)
        prob.sort(key=lambda p: p["id"])

        logging.info(f"{len(prob)} problems have been processed.")
        self.problems = prob

    def uniquify(self):
        logging.info("Creating a unique list of problems with number of solvers.")

        # format : [{count, prolem}]
        unique_problems = []
        cur_id = ""
        cur_ind = -1
        for problem in self.problems:
            if problem["id"] == cur_id:
                unique_problems[cur_ind]["count"] += 1
            else:
                cur_ind += 1
                cur_id = problem["id"]
                unique_problems.append({"count": 1, "problem": problem})
        unique_problems.sort(key=lambda p: p["count"], reverse=True)

        logging.info(
            f"{len(unique_problems)} unique problems have been found and sorted based on number of solvers.\n"
        )
        self.problems = unique_problems

    def print_top_5(self):
        logging.info(
            "Printig top 5 problems... (full problem list is in problems.json and problesm.txt)"
        )
        for pr in self.problems[:5]:
            print(f"Problem: {pr["problem"]["url"]}")
            print(f"Number of solvers: {pr["count"]}")


class Users:
    def __init__(self, *args, **kwargs):
        self.users = []
        self.user_count = 0

    def set_users(self, users):
        self.users = users
        self.user_count = len(users)

    def get_users(self):
        return self.users[:]

    def get_users_count(self):
        return self.user_count

    def fetch_users(self) -> None:
        url = f"{BASE_URL}/user.ratedList?activeOnly={ACTIVE_USERS}"

        logging.info("Fetching users...")
        try:
            res = requests.get(url)
            users = res.json()

            if users["status"] == "OK":
                users = list(
                    filter(
                        lambda user: is_in_rating_range(
                            user, USER_MIN_RATING, USER_MAX_RATING
                        ),
                        list(users["result"]),
                    )
                )
                users = list(map(lambda user: user["handle"], users))
                if len(users) > USER_COUNT:
                    users = users[:USER_COUNT]

                self.set_users(users)
            else:
                logging.info(f"Error fetching users.")
        except Exception as e:
            logging.info(f"Request failed: {e}")
        else:
            logging.info("Users are fetched successfully.")


class Menu:
    def __init__(self) -> None:
        self.options = {}
        self.options_count = 0

    def set_menu_options(self, options: list):
        self.options = options
        self.options_count = len(options)

    def get_menu(self):
        return self.options[:]

    def get_menu_option_count(self):
        return self.options_count


users_obj = Users()
problems_obj = Problems()
