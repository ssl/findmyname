"""Untappd: profile check on https://untappd.com/user/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Untappd username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://untappd.com/user/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
