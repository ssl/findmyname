"""Codeforces: profile check on https://codeforces.com/api/user.info?handles=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9_.-]{3,24}$")

SITE = Site(
    label="Codeforces username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://codeforces.com/api/user.info?handles={}',
        missing_status=400,
        missing_text='not found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
