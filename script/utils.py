import asyncio
import time

from .conf import RATE, SEM, LAST_CALL


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


def is_in_rating_range(user, min, max):
    if user["rating"] >= min and user["rating"] <= max:
        return True
    else:
        return False


def get_int(mi, ma) -> int | None:
    try:
        inp = int(input("Enter your choice: "))

        if inp == -1 or (inp >= mi and inp <= ma):
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
