"""HackerOne: profile check on https://hackerone.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="HackerOne username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://hackerone.com/{}',
        missing_text='Page not found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
