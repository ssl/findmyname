"""Roblox: ask the signup form whether a username can be registered."""

import re

import requests

from findmyname.site import RetryableError, Site, thread_session

VALID_PATTERN = re.compile(r"^(?!_)(?!.*_$)(?!.*_.*_)[a-z0-9_]{3,20}$")

URL = "https://auth.roblox.com/v1/usernames/validate"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
}


def check(username, config):
    """Return True if the username can be registered on Roblox."""
    params = {"Username": username, "Birthday": "2000-01-01", "Context": "Signup"}

    try:
        resp = thread_session().get(URL, params=params, headers=HEADERS,
                                    timeout=config.get("timeout_seconds", 15))
    except requests.RequestException as e:
        raise RetryableError(str(e)) from e

    if resp.status_code != 200:
        raise RetryableError(f"HTTP {resp.status_code}")

    try:
        code = resp.json()["code"]
    except (ValueError, KeyError, TypeError) as e:
        raise RetryableError("unexpected response") from e

    return code == 0


SITE = Site(
    label="Roblox username",
    pattern=VALID_PATTERN,
    check=check,
    defaults={"max_retries": 3, "retry_backoff": 5},
)
