"""pr0gramm: profile check on https://pr0gramm.com/api/profile/info?name=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="pr0gramm username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://pr0gramm.com/api/profile/info?name={}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
