"""TETR.IO: profile check on https://ch.tetr.io/api/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="TETR.IO username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://ch.tetr.io/api/users/{}',
        missing_text='No such user!',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
