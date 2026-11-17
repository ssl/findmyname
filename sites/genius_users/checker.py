"""Genius (Users): profile check on https://genius.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9]*?$")

SITE = Site(
    label="Genius (Users) username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://genius.com/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
