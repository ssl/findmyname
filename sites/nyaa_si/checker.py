"""Nyaa.si: profile check on https://nyaa.si/user/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Nyaa.si username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://nyaa.si/user/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
