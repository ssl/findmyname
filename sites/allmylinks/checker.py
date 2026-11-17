"""AllMyLinks: profile check on https://allmylinks.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,32}$")

SITE = Site(
    label="AllMyLinks username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://allmylinks.com/{}',
        missing_text='Page not found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
