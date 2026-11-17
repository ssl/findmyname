"""Atcoder: profile check on https://atcoder.jp/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Atcoder username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://atcoder.jp/users/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
