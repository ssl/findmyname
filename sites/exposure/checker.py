"""Exposure: profile check on https://<username>.exposure.co/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9-]{1,63}$")

SITE = Site(
    label="Exposure username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.exposure.co/',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
