"""Imgur: profile check on https://api.imgur.com/account/v1/accounts/<username>?client_id=546c25a59c58ad7"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Imgur username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://api.imgur.com/account/v1/accounts/{}?client_id=546c25a59c58ad7',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
