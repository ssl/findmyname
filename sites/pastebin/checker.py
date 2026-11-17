"""Pastebin: profile check on https://pastebin.com/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Pastebin username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://pastebin.com/u/{}',
        missing_text='Not Found (#404)',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
