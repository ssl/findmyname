"""d3RU: profile check on https://d3.ru/user/<username>/posts"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="d3RU username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://d3.ru/user/{}/posts',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
