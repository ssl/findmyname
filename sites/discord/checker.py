"""Discord: ask the signup form whether a username is taken."""

import re

import requests

from findmyname.site import RetryableError, Site, thread_session

VALID_PATTERN = re.compile(r"^(?!.*\.\.)[a-z0-9_.]{2,32}$")

URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
}


def check(username, config):
    """Return True if the username is available on Discord."""
    try:
        resp = thread_session().post(URL, json={"username": username}, headers=HEADERS,
                                     timeout=config.get("timeout_seconds", 15))
    except requests.RequestException as e:
        raise RetryableError(str(e)) from e

    if resp.status_code == 400:
        return False
    if resp.status_code != 200:
        raise RetryableError(f"HTTP {resp.status_code}")

    try:
        taken = resp.json()["taken"]
    except (ValueError, KeyError, TypeError) as e:
        raise RetryableError("unexpected response") from e

    return taken is False


SITE = Site(
    label="Discord username",
    pattern=VALID_PATTERN,
    check=check,
    defaults={"max_threads": 2, "max_retries": 5, "retry_backoff": 5},
)
