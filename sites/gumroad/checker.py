"""Gumroad: profile check on https://www.gumroad.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[^.]*?$")

SITE = Site(
    label="Gumroad username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.gumroad.com/{}',
        missing_text='Page not found (404) - Gumroad',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
