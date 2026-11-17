"""GitLab: profile check on https://gitlab.com/api/v4/users?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="GitLab username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://gitlab.com/api/v4/users?username={}',
        missing_text='[]',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
