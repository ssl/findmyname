"""Laracast: profile check on https://laracasts.com/@<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,}$")

SITE = Site(
    label="Laracast username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://laracasts.com/@{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
