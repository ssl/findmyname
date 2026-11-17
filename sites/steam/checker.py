"""Steam: a custom URL that shows the community error page is not in use."""

import re

import requests

from findmyname.site import RetryableError, Site, thread_session

VALID_PATTERN = re.compile(r"^[a-z0-9_-]+$")

ERROR_TITLE = "<title>Steam Community :: Error</title>"

HEADERS = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
}


def check(username, config):
    """Return True if the username is available on Steam."""
    url = "https://steamcommunity.com/id/" + username

    try:
        resp = thread_session().get(url, headers=HEADERS, timeout=config.get("timeout_seconds", 30))
    except requests.RequestException as e:
        raise RetryableError(str(e)) from e

    if resp.status_code != 200:
        raise RetryableError(f"HTTP {resp.status_code}")

    return ERROR_TITLE in resp.text


SITE = Site(
    label="Steam username",
    pattern=VALID_PATTERN,
    check=check,
    defaults={"max_retries": 3, "retry_backoff": 5},
)
