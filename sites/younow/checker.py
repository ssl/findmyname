"""YouNow: profile check on https://api.younow.com/php/api/broadcast/info/user=<username>/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="YouNow username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://api.younow.com/php/api/broadcast/info/user={}/',
        missing_text='No users found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
