"""Snapchat: profile check on https://www.snapchat.com/add/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z][a-z-_.]{3,15}$")

SITE = Site(
    label="Snapchat username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.snapchat.com/add/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
