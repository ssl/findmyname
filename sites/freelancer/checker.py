"""Freelancer: profile check on https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D=<username>&compact=true"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Freelancer username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D={}&compact=true',
        missing_text='"users":{}',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
