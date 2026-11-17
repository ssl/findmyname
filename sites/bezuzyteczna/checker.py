"""Bezuzyteczna: profile check on https://bezuzyteczna.pl/uzytkownicy/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Bezuzyteczna username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://bezuzyteczna.pl/uzytkownicy/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
