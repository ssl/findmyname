"""BoardGameGeek: profile check on https://api.geekdo.com/api/accounts/validate/username?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="BoardGameGeek username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://api.geekdo.com/api/accounts/validate/username?username={}',
        missing_text='"isValid":true',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
