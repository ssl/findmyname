"""StackBlitz: profile check on https://stackblitz.com/@<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="StackBlitz username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://stackblitz.com/@{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
