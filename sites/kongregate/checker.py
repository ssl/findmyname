"""Kongregate: profile check on https://www.kongregate.com/accounts/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

SITE = Site(
    label="Kongregate username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.kongregate.com/accounts/{}',
        missing_status=404,
        headers={'Accept': 'text/html'},
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
