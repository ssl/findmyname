"""Substack: profile check on https://<username>.substack.com/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,60}$")

SITE = Site(
    label="Substack username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.substack.com/',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
