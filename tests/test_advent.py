from datetime import datetime

import pytest

from advent_readme_stars.advent import most_recent_advent_year


@pytest.mark.parametrize(
    "now, expected",
    [
        (datetime(1999, 11, 30), 1998),
        (datetime(1999, 12, 1), 1999),
        (datetime(1999, 12, 31), 1999),
        (datetime(2000, 1, 1), 1999),
    ],
)
def test_most_recent_advent_year(now, expected):
    assert most_recent_advent_year(now) == expected
