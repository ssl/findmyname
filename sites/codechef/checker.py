"""Codechef: profile check on https://www.codechef.com/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Codechef username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.codechef.com/users/{}',
        missing_redirect=True,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
