"""Lobsters: profile check on https://lobste.rs/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,24}$")

SITE = Site(
    label="Lobsters username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://lobste.rs/u/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
