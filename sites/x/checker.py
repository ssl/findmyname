"""X (Twitter): profile check on https://x.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9_]{4,15}$")

SITE = Site(
    label="X (Twitter) username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://x.com/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
