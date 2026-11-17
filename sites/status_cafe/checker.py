"""Status Cafe: profile check on https://status.cafe/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Status Cafe username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://status.cafe/users/{}',
        missing_text='Page Not Found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
