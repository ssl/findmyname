"""Ionic Forum: profile check on https://forum.ionicframework.com/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Ionic Forum username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://forum.ionicframework.com/u/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
