"""Giphy: profile check on https://giphy.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Giphy username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://giphy.com/{}',
        missing_text='<title> GIFs - Find &amp; Share on GIPHY</title>',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
