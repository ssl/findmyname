"""n8n Community: profile check on https://community.n8n.io/u/<username>/summary"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="n8n Community username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://community.n8n.io/u/{}/summary',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
