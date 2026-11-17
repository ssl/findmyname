"""minds: profile check on https://www.minds.com/api/v3/register/validate?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="minds username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.minds.com/api/v3/register/validate?username={}',
        missing_text='"valid":true',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
