"""Gradle: profile check on https://plugins.gradle.org/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^(?!-)[a-zA-Z0-9-]{3,}(?<!-)$")

SITE = Site(
    label="Gradle username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://plugins.gradle.org/u/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
