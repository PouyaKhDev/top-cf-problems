import asyncio
import time

from conf import RATE, SEM, LAST_CALL, BASE_DIR


async def rate_limit():
    global LAST_CALL
    now = time.monotonic()
    wait = RATE - (now - LAST_CALL)
    if wait > 0:
        await asyncio.sleep(wait)
    LAST_CALL = time.monotonic()


async def fetch(session, url):
    async with SEM:
        await rate_limit()
        async with session.get(url) as response:
            if response.status == 429:
                await asyncio.sleep(2)
                return await fetch(session, url)
            return await response.json()


def is_in_rating_range(user, min, max) -> bool:
    if user["rating"] >= min and user["rating"] <= max:
        return True
    else:
        return False


def get_int(mi, ma, message="") -> int | None:

    if message:
        inp = int(input(message))
    else:
        inp = int(input("Enter your choice: "))
    try:

        if inp == -1 or (inp >= mi and inp <= ma):
            print("\n")
            return inp
        else:
            print(f"Your choice is not in the correct range [{mi}-{ma}]\n")
            return None

    except ValueError:
        print("Invalid number, Try again.\n")
        return None
    except Exception:
        print("Something went wrong, try again.\n")
        return None


def get_custom_users() -> list[str]:
    try:
        raw_users: list[str] = []
        with open(BASE_DIR / "custom_user.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                raw_users.extend([handle.strip() for handle in line.split(",")])

        users = list(filter(lambda u: u, raw_users))
        if len(users) == 0:
            print("custom_user.txt is empty.")
        return users
    except Exception as e:
        print(f"Something went wrong while opening the custom_user.txt: {e}")
        return users
