"""Carrd: profile check on https://<username>.carrd.co/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,50}$")

SITE = Site(
    label="Carrd username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.carrd.co/',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
