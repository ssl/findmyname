"""Codecademy: profile check on https://www.codecademy.com/profiles/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Codecademy username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.codecademy.com/profiles/{}',
        missing_text='This profile could not be found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
