"""Hacker News: the public API returns null for a user that does not exist."""

import re

import requests

from findmyname.site import RetryableError, Site, thread_session

VALID_PATTERN = re.compile(r"^[a-z0-9_-]{2,15}$")

URL = "https://hacker-news.firebaseio.com/v0/user/{}.json"


def check(username, config):
    """Return True if the username is available on Hacker News."""
    try:
        resp = thread_session().get(URL.format(username), timeout=config.get("timeout_seconds", 15))
    except requests.RequestException as e:
        raise RetryableError(str(e)) from e

    if resp.status_code != 200:
        raise RetryableError(f"HTTP {resp.status_code}")

    return resp.text.strip() == "null"


SITE = Site(
    label="Hacker News username",
    pattern=VALID_PATTERN,
    check=check,
    defaults={"max_retries": 3, "retry_backoff": 5},
)
