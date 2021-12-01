from dataclasses import dataclass
from typing import Generator

import requests

from advent_readme_stars.constants import SESSION_COOKIE, STARS_ENDPOINT, USER_ID


@dataclass(frozen=True, eq=True)
class DayProgress:
    day: int
    part_1: bool
    part_2: bool


def get_progress() -> Generator[DayProgress, None, None]:
    res = requests.get(STARS_ENDPOINT, cookies={"session": SESSION_COOKIE})
    res.raise_for_status()

    leaderboard_info = res.json()

    stars = leaderboard_info["members"][USER_ID]["completion_day_level"]

    for day, parts in stars.items():
        completed = parts.keys()
        yield DayProgress(
            day=int(day),
            part_1="1" in completed,
            part_2="2" in completed,
        )
