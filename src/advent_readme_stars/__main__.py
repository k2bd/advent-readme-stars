from typing import Dict, List, Optional
import datetime
import html
import json
import os
import time

import requests

from advent_readme_stars.advent import most_recent_advent_year
from advent_readme_stars.constants import README_LOCATION, SESSION_COOKIE, YEAR, ADVENT_URL, TABLE_MARKER

LEADERBOARDS = [
    {"id": 1739374, "name": "Team Default (Pakistan)"},
    {"id": 5206594, "name": "Team 2025"},
]

DATA_DIR = os.environ.get("INPUT_DATADIR", "data")

#: Number of rows rendered in the <noscript> fallback
FALLBACK_ROWS = 10


def years() -> List[str]:
    return [y.strip() for y in str(YEAR).split(",") if y.strip()]


def cache_path(year: str, board_id: int) -> str:
    return os.path.join(DATA_DIR, f"{year}-{board_id}.json")


def release_ts(year: str, day: int) -> int:
    """AoC puzzles unlock at midnight EST (05:00 UTC); EST has no DST in December."""
    return int(datetime.datetime(int(year), 12, day, 5, tzinfo=datetime.timezone.utc).timestamp())


def is_final(year: str, cached: dict) -> bool:
    """A past year's cache is final once it was fetched after that year's event ended."""
    if year == str(most_recent_advent_year()):
        return False
    fetched_at = cached.get("_fetched_at", 0)
    year_end = datetime.datetime(int(year) + 1, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
    return fetched_at >= year_end


def load_leaderboard(year: str, board_id: int) -> Optional[dict]:
    path = cache_path(year, board_id)
    cached = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        if is_final(year, cached):
            return cached

    if not SESSION_COOKIE:
        return cached

    url = f"{ADVENT_URL}/{year}/leaderboard/private/view/{board_id}.json"
    print(f"Fetching {url}")
    try:
        res = requests.get(url, cookies={"session": SESSION_COOKIE}, timeout=10)
        res.raise_for_status()
        data = res.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching {year} (board {board_id}): {e}")
        return cached

    data["_fetched_at"] = int(time.time())
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    return data


NAME_LINKS = {
    "support palestine": "https://www.linkedin.com/in/muhammad-saad-siddique/",
}


def linked_name(name: str) -> str:
    safe = html.escape(name)
    url = NAME_LINKS.get(name.strip().lower())
    if not url:
        return safe
    return f'<a class="person-link" href="{html.escape(url)}" target="_blank" rel="noreferrer">{safe}</a>'


def member_name(member: dict) -> str:
    return member.get("name") or f"Anonymous #{member['id']}"


def member_totals(member: dict, year: str) -> Dict[str, int]:
    stars = 0
    total = 0
    for day, parts in member.get("completion_day_level", {}).items():
        for part in parts.values():
            stars += 1
            total += max(0, part["get_star_ts"] - release_ts(year, int(day)))
    return {"stars": stars, "seconds": total}


def find_duplicates(boards: Dict[int, dict]) -> List[dict]:
    """Members with at least one star on more than one board, matched by AoC member id."""
    seen: Dict[str, dict] = {}
    for board in LEADERBOARDS:
        data = boards.get(board["id"])
        if not data:
            continue
        for member_id, member in data["members"].items():
            if not member.get("completion_day_level"):
                continue
            entry = seen.setdefault(member_id, {"id": int(member_id), "name": member_name(member), "boards": []})
            entry["boards"].append({"id": board["id"], "name": board["name"]})
    dupes = [m for m in seen.values() if len(m["boards"]) > 1]
    return sorted(dupes, key=lambda m: m["name"].lower())


def format_duration(seconds: int) -> str:
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    clock = f"{hours:02}:{minutes:02}:{secs:02}"
    return f"{days}d {clock}" if days else clock


def fallback_table(year: str, boards: Dict[int, dict]) -> List[str]:
    merged: Dict[str, dict] = {}
    for data in boards.values():
        if data:
            for member_id, member in data["members"].items():
                merged.setdefault(member_id, member)

    rows = []
    for member in merged.values():
        totals = member_totals(member, year)
        if totals["stars"]:
            rows.append((totals["seconds"], member_name(member), totals["stars"]))
    rows.sort()

    lines = [
        "<noscript>",
        f"<div class='section__header'><h2>{year} top {FALLBACK_ROWS} by total time</h2></div>",
        "<div class='table__wrap'><table><thead><tr><th>Rank</th><th>Name</th><th>Stars</th><th>Total time</th></tr></thead><tbody>",
    ]
    for rank, (seconds, name, stars) in enumerate(rows[:FALLBACK_ROWS], start=1):
        lines.append(f"<tr><td>{rank}</td><td>{linked_name(name)}</td><td>{stars}</td><td>{format_duration(seconds)}</td></tr>")
    lines.append("</tbody></table></div>")
    lines.append("</noscript>")
    return lines


def write_json(name: str, payload) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, name), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def generate_data() -> List[str]:
    """Fetch/cache every board for every year, write manifest and duplicates, return the fallback HTML."""
    manifest = {
        "generated_at": int(time.time()),
        "boards": [{"id": b["id"], "name": b["name"]} for b in LEADERBOARDS],
        "years": [],
    }
    duplicates: Dict[str, List[dict]] = {}
    fallback: List[str] = []

    for year in sorted(years(), reverse=True):
        boards = {b["id"]: load_leaderboard(year, b["id"]) for b in LEADERBOARDS}
        available = [board_id for board_id, data in boards.items() if data]
        if not available:
            print(f"No data for {year}, skipping")
            continue

        num_days = max(boards[board_id].get("num_days", 25) for board_id in available)
        manifest["years"].append({"year": year, "num_days": num_days, "boards": available})

        dupes = find_duplicates(boards)
        duplicates[year] = dupes
        if dupes:
            print(f"\n{year}: {len(dupes)} member(s) on more than one leaderboard")
            for d in dupes:
                print(f"  {d['name']} (id {d['id']}): {', '.join(b['name'] for b in d['boards'])}")

        if not fallback:
            fallback = fallback_table(year, boards)

    write_json("manifest.json", manifest)
    write_json("duplicates.json", duplicates)
    return fallback


def update_readme(readme: List[str], inserted: List[str]) -> List[str]:
    """Replace everything between the first two TABLE_MARKER lines with `inserted`."""
    markers = [i for i, line in enumerate(readme) if line.strip() == TABLE_MARKER]
    if not markers:
        return readme
    start = markers[0]
    end = markers[1] if len(markers) > 1 else start
    return readme[: start + 1] + inserted + [TABLE_MARKER] + readme[end + 1:]


if __name__ == "__main__":
    if not SESSION_COOKIE:
        print("SESSION_COOKIE is not set; using cached leaderboard data only.")

    fallback = generate_data()

    try:
        with open(README_LOCATION, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"{README_LOCATION} not found, skipping HTML fallback update.")
    else:
        with open(README_LOCATION, "w", encoding="utf-8") as f:
            f.write("\n".join(update_readme(lines, fallback)) + "\n")
        print(f"\nUpdated {README_LOCATION}.")
