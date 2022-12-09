import os.path
from typing import List

from advent_readme_stars.constants import (
    ADVENT_URL,
    HEADER_PREFIX,
    README_LOCATION,
    SOLUTION_LOCATIONS,
    SOLUTION_PADDING,
    STAR_SYMBOL,
    TABLE_MARKER,
    YEAR,
)
from advent_readme_stars.progress import get_progress


def remove_existing_table(lines: List[str]) -> List[str]:
    """
    If there's an existing table, it should be between two table markers.
    If that's the case, remove the existing table and return a single table
    marker in its place. If not, just return the original content.
    """
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and line.strip() == TABLE_MARKER:
            start = i
            continue
        if start is not None and line.strip() == TABLE_MARKER:
            end = i
            break

    if start is not None and end is not None:
        return lines[:start] + lines[end:]
    return lines


def insert_table(lines: List[str]) -> List[str]:
    """
    Search the lines for a table marker, and insert a table there.
    """
    table_location = None
    for i, line in enumerate(lines):
        if line.strip() == TABLE_MARKER:
            table_location = i
            break
    else:
        return lines

    to_insert = [
        TABLE_MARKER,
        f"{HEADER_PREFIX} {YEAR} Results",
        "",
        "| Day | Part 1 | Part 2 |",
        "| :---: | :---: | :---: |",
    ]
    stars_info = sorted(list(get_progress()), key=lambda p: p.day)

    for star_info in stars_info:
        day_url = f"{ADVENT_URL}/{YEAR}/day/{star_info.day}"
        day_text = f"[Day {star_info.day}]({day_url})"
        part_1_text = STAR_SYMBOL if star_info.part_1 else " "
        part_2_text = STAR_SYMBOL if star_info.part_2 else " "
        to_insert.append(f"| {day_text} | {part_1_text} | {part_2_text} |")

    return lines[:table_location] + to_insert + lines[table_location:]


def insert_solutions_table(lines: List[str]) -> List[str]:
    """
    Search the lines for a table marker,
    and insert a table with links to the solutions there.
    """
    table_location = None
    for i, line in enumerate(lines):
        if line.strip() == TABLE_MARKER:
            table_location = i
            break
    else:
        return lines

    to_insert = [
        TABLE_MARKER,
        f"{HEADER_PREFIX} {YEAR} Results",
        "",
        "| Day | Solution | Part 1 | Part 2 |",
        "| :---: | :---: | :---: | :---: |",
    ]
    stars_info = sorted(list(get_progress()), key=lambda p: p.day)

    for star_info in stars_info:
        day_url = f"{ADVENT_URL}/{YEAR}/day/{star_info.day}"
        day_text = f"[Day {star_info.day}]({day_url})"
        part_1_text = STAR_SYMBOL if star_info.part_1 else " "
        part_2_text = STAR_SYMBOL if star_info.part_2 else " "
        solution = get_solution(star_info.day)
        to_insert.append(f"| {day_text} | {solution} | {part_1_text} | {part_2_text} |")

    return lines[:table_location] + to_insert + lines[table_location:]


def get_solution(day: int) -> str:
    """
    Gets the solution text for a specific day
    """
    day_text = str(day).rjust(2 if SOLUTION_PADDING.lower() == "true" else 1, "0")
    solution_rel_path = SOLUTION_LOCATIONS.format(day_text)
    readme_dir = README_LOCATION.removesuffix(os.path.basename(README_LOCATION))
    solution_location = os.path.join(readme_dir, solution_rel_path)
    if os.path.exists(solution_location):
        file_name = os.path.basename(solution_location)
        return f"[{file_name}]({solution_rel_path})"
    else:
        return ""


def update_readme(readme: List[str]) -> List[str]:
    """
    Take the contents of a readme file and update them
    """
    reduced = remove_existing_table(readme)
    if SOLUTION_LOCATIONS != "":
        return insert_solutions_table(reduced)
    else:
        return insert_table(reduced)
