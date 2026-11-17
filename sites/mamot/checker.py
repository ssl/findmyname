"""Mamot: profile check on https://mamot.fr/@<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9_]{1,30}$")

SITE = Site(
    label="Mamot username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://mamot.fr/@{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
