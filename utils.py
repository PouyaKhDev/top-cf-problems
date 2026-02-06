import aiohttp
import asyncio
import time
import json

import model
from conf import RATE, SEM


async def rate_limit():
    now = time.monotonic()
    wait = RATE - (now - model.LAST_CALL)
    if wait > 0:
        await asyncio.sleep(wait)
    model.LAST_CALL = time.monotonic()


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
