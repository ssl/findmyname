"""CashApp: profile check on https://cash.app/$<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="CashApp username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://cash.app/${}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
