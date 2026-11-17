"""Memrise: profile check on https://www.memrise.com/user/<username>/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Memrise username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.memrise.com/user/{}/',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
