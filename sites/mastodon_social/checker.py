"""mastodon.social: profile check on https://mastodon.social/@<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="mastodon.social username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://mastodon.social/@{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
