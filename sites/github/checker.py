"""GitHub: compare the avatar of a username with the default 'not found' avatar."""

import hashlib
import re

import requests

from findmyname.site import RetryableError, Site, thread_session

VALID_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$")

DEFAULT_AVATAR_MD5 = "2785b1bedaed3962692a1850a4c50faa"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


def check(username, config):
    """Return True if the username is available on GitHub."""
    url = f"https://avatars.githubusercontent.com/{username}?s=1"

    try:
        resp = thread_session().get(url, headers=HEADERS, timeout=config.get("timeout_seconds", 10))
    except requests.RequestException as e:
        raise RetryableError(str(e)) from e

    if resp.status_code != 200:
        raise RetryableError(f"HTTP {resp.status_code}")

    return hashlib.md5(resp.content).hexdigest() == DEFAULT_AVATAR_MD5


SITE = Site(
    label="GitHub username",
    pattern=VALID_PATTERN,
    check=check,
    defaults={"max_retries": 5, "retry_backoff": 2},
)
