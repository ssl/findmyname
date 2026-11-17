"""Dribbble: profile check on https://dribbble.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

SITE = Site(
    label="Dribbble username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://dribbble.com/{}',
        missing_text='Whoops, that page is gone.',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
