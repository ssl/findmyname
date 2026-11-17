"""SoylentNews: profile check on https://soylentnews.org/~<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="SoylentNews username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://soylentnews.org/~{}',
        missing_text='The user you requested does not exist, no matter how much you wish this might be the case.',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
