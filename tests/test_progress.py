from advent_readme_stars.progress import DayProgress, get_progress

from .helpers import EXAMPLE_DATA_1, EXAMPLE_DATA_2, EXAMPLE_DATA_3, mock_responses


def test_get_progress_example1():
    with mock_responses(EXAMPLE_DATA_1):
        stars = set(get_progress())

    assert stars == {
        DayProgress(day=1, part_1=True, part_2=True),
    }


def test_get_progress_example2():
    with mock_responses(EXAMPLE_DATA_2):
        stars = set(get_progress())

    assert stars == {
        DayProgress(day=1, part_1=True, part_2=True),
        DayProgress(day=2, part_1=True, part_2=True),
        DayProgress(day=3, part_1=True, part_2=True),
        DayProgress(day=4, part_1=True, part_2=True),
        DayProgress(day=5, part_1=True, part_2=True),
        DayProgress(day=6, part_1=True, part_2=True),
    }


def test_get_progress_example3():
    with mock_responses(EXAMPLE_DATA_3):
        stars = set(get_progress())

    assert stars == {
        DayProgress(day=1, part_1=True, part_2=True),
        DayProgress(day=2, part_1=True, part_2=False),
        DayProgress(day=3, part_1=True, part_2=True),
        DayProgress(day=4, part_1=True, part_2=False),
        DayProgress(day=5, part_1=True, part_2=True),
        DayProgress(day=6, part_1=True, part_2=True),
    }
