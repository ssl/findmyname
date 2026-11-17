"""Instagram: ask the signup form whether a username can be registered."""

import re

import requests

from findmyname.site import RetryableError, Site

VALID_PATTERN = re.compile(r"^(?!\.)(?!.*\.\.)(?!.*^\d+$)[a-z0-9.]+(?<!\.)$")

URL = "https://www.instagram.com:443/accounts/web_create_ajax/attempt/"

HEADERS = {
    "X-Ig-Www-Claim": "0", "X-Instagram-Ajax": "ee0117db2fab",
    "Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest", "X-Asbd-Id": "198387",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "X-Csrftoken": "POttsFJopRtOI0HqAqrcZDXq6nX6haa2", "X-Ig-App-Id": "936619743392459",
    "Sec-Gpc": "1", "Origin": "https://www.instagram.com",
    "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty", "Referer": "https://www.instagram.com/accounts/emailsignup/",
    "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "close",
}


def get_random_proxy(config):
    """Return the proxy to use. Edit this to rotate through a proxy list."""
    return config.get("proxy", "")


def check(username, config):
    """Return True if the username is available on Instagram."""
    data = {"email": "", "username": username, "first_name": "", "opt_into_one_tap": "false"}
    proxy = get_random_proxy(config)
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

    try:
        resp = requests.post(URL, headers=HEADERS, data=data, proxies=proxies,
                             timeout=config.get("timeout_seconds", 10))
    except requests.RequestException as e:
        raise RetryableError(str(e)) from e

    if "Try again later" in resp.text:
        raise RetryableError("proxy is rate limited")

    try:
        errors = resp.json().get("errors", {})
    except (ValueError, AttributeError) as e:
        raise RetryableError("proxy blocked") from e

    if not isinstance(errors, dict) or errors.get("email") is None:
        raise RetryableError("proxy blocked")

    return errors.get("username") is None


SITE = Site(
    label="Instagram username",
    pattern=VALID_PATTERN,
    check=check,
    defaults={"max_retries": 25, "retry_backoff": 0},
)
