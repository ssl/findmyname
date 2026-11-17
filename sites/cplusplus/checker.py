"""Cplusplus: profile check on https://cplusplus.com/user/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Cplusplus username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://cplusplus.com/user/{}',
        missing_text='<title>404 Page Not Found</title>',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
