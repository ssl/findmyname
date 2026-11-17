"""LOR: profile check on https://www.linux.org.ru/people/<username>/profile"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="LOR username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.linux.org.ru/people/{}/profile',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
