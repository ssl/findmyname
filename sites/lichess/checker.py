"""Lichess: profile check on https://lichess.org/api/user/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{0,28}[a-z0-9]$")

SITE = Site(
    label="Lichess username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://lichess.org/api/user/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
