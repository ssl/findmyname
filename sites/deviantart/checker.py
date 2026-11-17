"""DeviantArt: profile check on https://www.deviantart.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9-]{3,20}$")

SITE = Site(
    label="DeviantArt username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.deviantart.com/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
