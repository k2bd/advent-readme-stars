import os
from contextlib import contextmanager
from typing import Generator

import responses
from responses import RequestsMock

from advent_readme_stars.constants import STARS_ENDPOINT

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EXAMPLE_DATA_1 = os.path.join(_DATA_DIR, "example1.json")
EXAMPLE_DATA_2 = os.path.join(_DATA_DIR, "example2.json")
EXAMPLE_DATA_3 = os.path.join(_DATA_DIR, "example3.json")


@contextmanager
def mock_responses(
    leaderboard_file: str,
    require_all: bool = False,
) -> Generator[RequestsMock, None, None]:
    with open(leaderboard_file) as f:
        body = f.read()

    with RequestsMock(assert_all_requests_are_fired=require_all) as r:
        r.add(responses.GET, STARS_ENDPOINT, body=body)

        yield r
