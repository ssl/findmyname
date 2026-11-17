"""VK: profile check on https://vk.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z][a-z0-9_.]{4,31}$")

SITE = Site(
    label="VK username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://vk.com/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
