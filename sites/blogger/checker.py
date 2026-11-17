"""Blogger: profile check on https://<username>.blogspot.com"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

SITE = Site(
    label="Blogger username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.blogspot.com',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
