"""Linktree: profile check on https://linktr.ee/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[\w\.]{2,30}$")

SITE = Site(
    label="Linktree username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://linktr.ee/{}',
        missing_text='"statusCode":404',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
