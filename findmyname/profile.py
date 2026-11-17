"""Profile check: a username counts as available when its profile page does not exist."""

import requests

from .site import RetryableError, thread_session

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"


def profile_check(url, missing_status=None, missing_text=None, missing_redirect=False,
                  headers=None, timeout=15):
    """Build a check function for a profile URL, with `{}` for the username."""
    if isinstance(missing_text, str):
        missing_text = (missing_text,)
    request_headers = {"User-Agent": USER_AGENT, **(headers or {})}

    def check(username, config):
        try:
            resp = thread_session().get(
                url.format(username),
                headers=request_headers,
                timeout=config.get("timeout_seconds", timeout),
                allow_redirects=not missing_redirect,
            )
        except requests.RequestException as e:
            raise RetryableError(str(e)) from e

        status = resp.status_code

        if missing_redirect:
            if 300 <= status < 400:
                return True
            if status == 200:
                return False
        elif missing_text and missing_status:
            if status == missing_status and any(text in resp.text for text in missing_text):
                return True
            if status == 200:
                return False
        elif missing_text:
            if status in (200, 404):
                return any(text in resp.text for text in missing_text)
        else:
            if status == missing_status:
                return True
            if status == 200:
                return False

        raise RetryableError(f"HTTP {status}")

    return check
