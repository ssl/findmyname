"""Joplin Forum: profile check on https://discourse.joplinapp.org/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Joplin Forum username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://discourse.joplinapp.org/u/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
