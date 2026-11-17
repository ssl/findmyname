"""Genius (Artists): profile check on https://genius.com/artists/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9]{5,50}$")

SITE = Site(
    label="Genius (Artists) username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://genius.com/artists/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
