"""Tenor: profile check on https://tenor.com/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[A-Za-z0-9_]{2,32}$")

SITE = Site(
    label="Tenor username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://tenor.com/users/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
