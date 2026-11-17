"""OurDJTalk: profile check on https://ourdjtalk.com/members?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="OurDJTalk username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://ourdjtalk.com/members?username={}',
        missing_text='The specified member cannot be found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
