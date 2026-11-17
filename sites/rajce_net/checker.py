"""Rajce.net: profile check on https://<username>.rajce.idnes.cz/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[\w@-]+?$")

SITE = Site(
    label="Rajce.net username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.rajce.idnes.cz/',
        missing_status=410,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
