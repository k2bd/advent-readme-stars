# Advent README Stars

[![CI](https://github.com/k2bd/advent-readme-stars/actions/workflows/ci.yml/badge.svg)](https://github.com/k2bd/advent-readme-stars/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/k2bd/advent-readme-stars/branch/main/graph/badge.svg?token=J5FA3JU4OI)](https://codecov.io/gh/k2bd/advent-readme-stars)

This [action](https://github.com/marketplace/actions/advent-readme-stars) adds and maintains a stars report in your README based on your [Advent of Code](https://adventofcode.com/) progress.

## Example Table

<!--- advent_readme_stars table example --->
### 2022 Results

| Day | Part 1 | Part 2 |
| :---: | :---: | :---: |
| [Day 1](https://adventofcode.com/2022/day/1) | ⭐ | ⭐ |
| [Day 2](https://adventofcode.com/2022/day/2) | ⭐ | ⭐ |
| [Day 3](https://adventofcode.com/2022/day/3) | ⭐ | ⭐ |
| [Day 4](https://adventofcode.com/2022/day/4) | ⭐ | ⭐ |
| [Day 5](https://adventofcode.com/2022/day/5) | ⭐ | ⭐ |
| [Day 6](https://adventofcode.com/2022/day/6) | ⭐ | ⭐ |
| [Day 7](https://adventofcode.com/2022/day/7) | ⭐ | ⭐ |
| [Day 8](https://adventofcode.com/2022/day/8) | ⭐ | ⭐ |
| [Day 9](https://adventofcode.com/2022/day/9) | ⭐ | ⭐ |
| [Day 10](https://adventofcode.com/2022/day/10) | ⭐ | ⭐ |
<!--- advent_readme_stars table example --->

## Quickstart

Add this line somewhere in your `README.md`:

```markdown
<!--- advent_readme_stars table --->
```

Make a note of your user ID and add your session cookie to your repo as a secret called `AOC_SESSION`.
To see how to find these values, see those sections in the spec below.

Add this action to your repo as `.github/workflows/readme-stars.yml`, pasting in your user ID and the leaderboard ID to pull data from (or remove this argument to default to your own private leaderboard):

```yml
name: Update README ⭐
on:
  schedule:
    - cron: "51 */4 * * *"  # Every 4 hours
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3
      - uses: k2bd/advent-readme-stars@v1
        with:
          userId: 1234567
          leaderboardId: 9876543
          sessionCookie: ${{ secrets.AOC_SESSION }}
      - uses: stefanzweifel/git-auto-commit-action@v5 # use v5
        with:
          commit_message: Update README stars
```

If you want to adjust the cron expression, please remember to schedule your jobs such that you respect the Advent of Code request of running automated requests at a rate of no more than 1 per 15 minutes.

## Action Spec

### `userId`

**Required**

Your Advent of Code user ID.
To get this, go to your Go to [settings](https://adventofcode.com/2021/settings).
The user ID is displayed in the first option of the question "What would you like to be called?":

```
( ) (anonymous user #<your ID>)
( ) ....
```


### `sessionCookie`

**Required**

Your Advent of Code session cookie.
To get this, press F12 anywhere on the Advent of Code website to open your browser developer tools.
Look in your Cookies under the Application or Storage tab, and copy out the session cookie.
This should be stored as a repository secret, not pasted directly into the action or any other publicly viewable place.

### `leaderboardId`

*Optional* - default `userId` value

Your Advent of Code leaderboard ID.
To get this, go to your Go to [leaderboard](https://adventofcode.com/2020/leaderboard/private) and press 'View' (or 'Create' if you haven't yet created a private leaderboard).
The leaderboard ID is at the end of the URL:

```
https://adventofcode.com/2021/leaderboard/private/view/(leaderboard ID)
```

### `tableMarker`

*Optional* - default `<!--- advent_readme_stars table --->`

This is the string that marks the table location in your README file. The action will only work if it finds this marker in your file, on its own line. You should only add it once, and then let the action do its work.

Change this value if, for example, you'd like different actions maintaining different year results. However, remember to schedule your jobs such that you respect the Advent of Code request of running automated requests at a rate of no more than 1 per 15 minutes.

### `starSymbol`

*Optional* - default ⭐

The symbol that will mark completed parts in your table.

### `year`

*Optional* - default is year of the most recent advent

Year to get results for.
By default, it will get results for the year of the most recent advent.
That is, this year if it's December, otherwise last year.

### `headerPrefix`

*Optional* - default `##`

Prefix for the section header added before the table.
Should be some kind of Markdown header level.

### `readmeLocation`

*Optional* - default `README.md`

Location of the README file to edit.

### `solutionLocations`

*Optional* - default is none

Location of the solution files relative to the `readmeLocation`,
the following placeholders can be used:

- `{d}` The day of the solution (e.g. 3, 5 and 10)
- `{dd}` The padded day of the solution (e.g. 03, 05 and 10)
- `{yyyy}` The year of the solution (e.g. 2021 or 2023)
- `{yy}` The truncated year of the solution (e.g. 21 or 23)

## Like this project?

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png)](https://www.buymeacoffee.com/k2bd)
