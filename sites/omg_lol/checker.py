"""omg.lol: profile check on https://api.omg.lol/address/<username>/availability"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="omg.lol username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://api.omg.lol/address/{}/availability',
        missing_text='"available": true',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
