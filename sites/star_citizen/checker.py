"""Star Citizen: profile check on https://robertsspaceindustries.com/citizens/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Star Citizen username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://robertsspaceindustries.com/citizens/{}',
        missing_text='404',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
