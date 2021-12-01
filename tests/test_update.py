import pytest

from advent_readme_stars.constants import TABLE_MARKER
from advent_readme_stars.update import (
    insert_table,
    remove_existing_table,
    update_readme,
)

DEFAULT_TABLE_CONTENT = [
    "## 2019 Results",
    "",
    "| Day | Part 1 | Part 2 |",
    "| :---: | :---: | :---: |",
    "| [Day 1](http://fake.site.k2bd.dev/2019/day/1) | ⭐ | ⭐ |",
    "| [Day 2](http://fake.site.k2bd.dev/2019/day/2) | ⭐ |   |",
    "| [Day 3](http://fake.site.k2bd.dev/2019/day/3) | ⭐ | ⭐ |",
    "| [Day 4](http://fake.site.k2bd.dev/2019/day/4) | ⭐ |   |",
    "| [Day 5](http://fake.site.k2bd.dev/2019/day/5) | ⭐ | ⭐ |",
    "| [Day 6](http://fake.site.k2bd.dev/2019/day/6) | ⭐ | ⭐ |",
]


@pytest.mark.parametrize(
    "lines, expected",
    [
        (
            [
                "AAAAA",
                TABLE_MARKER,
                "BBBBB",
                "CCCCC",
                "DDDDD",
                TABLE_MARKER,
                "EEEEE",
            ],
            [
                "AAAAA",
                TABLE_MARKER,
                "EEEEE",
            ],
        ),
        (
            [
                TABLE_MARKER,
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
            [
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
                TABLE_MARKER,
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
            ],
        ),
        (
            [
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
            ],
            [
                TABLE_MARKER,
            ],
        ),
        (
            [
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
            [
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                TABLE_MARKER,
                "DDDDD",
                "EEEEE",
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                TABLE_MARKER,
                "DDDDD",
                "EEEEE",
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
        ),
    ],
)
def test_remove_existing_table(lines, expected):
    assert remove_existing_table(lines) == expected


@pytest.mark.parametrize(
    "lines, expected",
    [
        (
            [
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
            [
                TABLE_MARKER,
                *DEFAULT_TABLE_CONTENT,
                TABLE_MARKER,
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                TABLE_MARKER,
                "DDDDD",
                "EEEEE",
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                TABLE_MARKER,
                *DEFAULT_TABLE_CONTENT,
                TABLE_MARKER,
                "DDDDD",
                "EEEEE",
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
                TABLE_MARKER,
                *DEFAULT_TABLE_CONTENT,
                TABLE_MARKER,
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
        ),
    ],
)
def test_insert_table(lines, expected, default_stars_response):
    assert insert_table(lines) == expected


@pytest.mark.parametrize(
    "lines, expected",
    [
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                TABLE_MARKER,
                "FFFFF",
                "GGGGG",
                "HHHHH",
                TABLE_MARKER,
                "DDDDD",
                "EEEEE",
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                TABLE_MARKER,
                *DEFAULT_TABLE_CONTENT,
                TABLE_MARKER,
                "DDDDD",
                "EEEEE",
            ],
        ),
        (
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
            [
                "AAAAA",
                "BBBBB",
                "CCCCC",
                "DDDDD",
                "EEEEE",
            ],
        ),
    ],
)
def test_update_readme(lines, expected, default_stars_response):
    assert update_readme(lines) == expected
