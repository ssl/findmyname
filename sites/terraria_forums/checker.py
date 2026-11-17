"""Terraria Forums: profile check on https://forums.terraria.org/index.php?search/42798315/&c[users]=<username>&o=relevance"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Terraria Forums username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://forums.terraria.org/index.php?search/42798315/&c[users]={}&o=relevance',
        missing_text='The following members could not be found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
