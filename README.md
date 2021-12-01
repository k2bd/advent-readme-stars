# Advent README Stars

This project adds a stars report to your README based on your advent of code progress.

## Quickstart

Add this line somewhere in your README.md:

```markdown
<!--- advent_readme_stars table --->
```

Make a note of your user ID and add your session cookie to your repo as a secret called `AOC_SESSION`.
To see how to find these values, see those sections in the spec below.

Add this action to your repo as `.github/workflows/readme-stars.yml`, pasting in yout user ID instead of 1234567:

```yml
name: Update README ⭐
on:
  schedule:
    - cron: "51 */4 * * *"  # Every 4 hours
  workflow_dispatch:

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: k2bd/advent-readme-stars@v1
        with:
          userId: 1234567
          sessionCookie: ${{ secrets.AOC_SESSION }}
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: Update README stars
          file_pattern: README.md
```

## Action Spec

### `userId`

**Required**

Your Advent of Code user ID.
To get this, go to your Go to [leaderboard](https://adventofcode.com/2020/leaderboard/private) and press 'View'.
Your ID is at the end of the URL:

```
https://adventofcode.com/2021/leaderboard/private/view/(your ID)
```

### `sessionCookie`

**Required**

Your Advent of Code session cookie.
To get this, press F12 anywhere on the Advent of Code website to open your browser developer tools.
Look in your Cookies under the Application or Storage tab, and copy out the session cookie.
This should be stored as a repository secret, not pasted directly into the action or any other publicly viewable place.

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

## Example Table

<!--- advent_readme_stars table --->

## Like this project?

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png)](https://www.buymeacoffee.com/k2bd)
