"""HackerRank: profile check on https://hackerrank.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[^.]*?$")

SITE = Site(
    label="HackerRank username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://hackerrank.com/{}',
        missing_text='Something went wrong',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
