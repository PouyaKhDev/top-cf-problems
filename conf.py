import asyncio

from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent
BASE_URL = "https://codeforces.com/api"

SEM = asyncio.Semaphore(2)
RATE = 0.3

USER_COUNT = 200
ACTIVE_USERS = True
USER_MIN_RATING = 1400
USER_MAX_RATING = 1500

PROBLEM_COUNT = 100
PROBLEM_MIN_RATING = 1200
PROBLEM_MAX_RATING = 9999

YEARS_BACK = 1
START_TIME_STAMPS = (datetime.now() - timedelta(days=365 * YEARS_BACK)).timestamp()
