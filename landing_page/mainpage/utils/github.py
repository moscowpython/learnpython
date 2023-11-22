import datetime

import requests
from memoize import memoize


@memoize(timeout=24 * 60 * 60)
def fetch_last_commit_date_from_github_repo(
    owner: str,
    repo_name: str,
    timeout_msec: int = 500,
) -> datetime.datetime | None:
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/commits",
        timeout=timeout_msec / 1000,
    )
    if not response:
        return None
    all_commits = response.json()
    if not isinstance(all_commits, list) or not all_commits:
        return None
    last_commit = all_commits[0]
    raw_commit_date = last_commit.get("commit", {}).get("author", {}).get("date")
    try:
        last_commit_date = datetime.datetime.fromisoformat(raw_commit_date) if raw_commit_date else None
    except ValueError:
        last_commit_date = None

    return last_commit_date
