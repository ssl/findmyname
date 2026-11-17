"""Mydramalist: profile check on https://www.mydramalist.com/profile/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Mydramalist username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.mydramalist.com/profile/{}',
        missing_text='The requested page was not found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
