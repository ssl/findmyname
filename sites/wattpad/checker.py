"""Wattpad: profile check on https://www.wattpad.com/api/v3/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Wattpad username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.wattpad.com/api/v3/users/{}',
        missing_status=400,
        missing_text='"NotFound"',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
