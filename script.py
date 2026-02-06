import requests
import aiohttp
import time
import asyncio
import json
import logging


import model
from conf import (
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
from utils import is_in_rating_range, fetch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


def fetch_users() -> None:
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

            model.set_users(users)
        else:
            logging.info(f"Error fetching users.")
    except Exception as e:
        logging.info(f"Request failed: {e}")
    else:
        logging.info("Users are fetched successfully.")


async def fetch_and_save_problems():
    users = model.get_users()
    urls = [
        f"https://codeforces.com/api/user.status?handle={handle}" for handle in users
    ]

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
        logging.info("Problems are fetched successfully.")

    logging.info("Processing problems...")

    problems = []
    for sub in results:
        if (
            sub["verdict"] != "OK"
            or sub["creationTimeSeconds"] < START_TIME_STAMPS
            or "rating" not in sub["problem"]
            or sub["problem"]["rating"] < PROBLEM_MIN_RATING
            or sub["problem"]["rating"] > PROBLEM_MAX_RATING
        ):
            continue

        prob = {
            "contest_id": sub["contestId"],
            "index": sub["problem"]["index"],
            "rating": sub["problem"]["rating"],
            "id": f"{sub["problem"]["contestId"]}#{sub["problem"]["index"]}",
            "url": f"https://codeforces.com/contest/{sub["contestId"]}/problem/{sub["problem"]["index"]}",
        }

        problems.append(prob)
    problems.sort(key=lambda p: p["id"])

    logging.info(f"{len(problems)} problems have been found.")

    logging.info("Creating a unique list of problems with number of solvers.")

    # format : [{count, prolem}]
    unique_problems = []
    cur_id = ""
    cur_ind = -1
    for problem in problems:
        if problem["id"] == cur_id:
            unique_problems[cur_ind]["count"] += 1
        else:
            cur_ind += 1
            cur_id = problem["id"]
            unique_problems.append({"count": 1, "problem": problem})
    unique_problems.sort(key=lambda p: p["count"], reverse=True)

    logging.info(
        f"{len(unique_problems)} unique problems have been found and sorted based on number of solvers."
    )

    if len(unique_problems) > PROBLEM_COUNT:
        model.set_problems(unique_problems[:PROBLEM_COUNT])
    else:
        model.set_problems(unique_problems)

    logging.info(
        f"Saving top {len(model.get_problems())} problems in 'static/problems.json' and 'static/problems.txt'"
    )
    model.save_problems()
    logging.info("Problems are saved successfully.")


def main():
    fetch_users()
    asyncio.run(fetch_and_save_problems())


main()
