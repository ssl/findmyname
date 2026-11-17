"""Duolingo: profile check on https://www.duolingo.com/2017-06-30/users?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Duolingo username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.duolingo.com/2017-06-30/users?username={}',
        missing_status=200,
        missing_text='{"users":[]}',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
