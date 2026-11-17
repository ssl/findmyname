"""Kick: profile check on https://kick.com/api/v2/channels/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9_]{4,25}$")

SITE = Site(
    label="Kick username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://kick.com/api/v2/channels/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
