"""Wikidot: profile check on http://www.wikidot.com/user:info/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Wikidot username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='http://www.wikidot.com/user:info/{}',
        missing_text='User does not exist.',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
