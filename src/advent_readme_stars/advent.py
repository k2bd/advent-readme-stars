from datetime import datetime


def most_recent_advent_year(time: datetime = None) -> int:
    """
    Get the year of the most recent advent
    """
    time = time or datetime.now()

    if time.month < 12:
        return time.year - 1
    return time.year
