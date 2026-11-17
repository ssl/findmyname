"""WordPress: profile check on https://<username>.wordpress.com/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

SITE = Site(
    label="WordPress username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.wordpress.com/',
        missing_redirect=True,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
