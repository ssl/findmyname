"""Discuss.Elastic.co: profile check on https://discuss.elastic.co/u/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Discuss.Elastic.co username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://discuss.elastic.co/u/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
