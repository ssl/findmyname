"""Ultimate-Guitar: profile check on https://ultimate-guitar.com/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Ultimate-Guitar username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://ultimate-guitar.com/u/{}',
        missing_status=410,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
