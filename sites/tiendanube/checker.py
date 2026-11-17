"""Tiendanube: profile check on https://<username>.mitiendanube.com/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Tiendanube username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.mitiendanube.com/',
        missing_status=410,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
