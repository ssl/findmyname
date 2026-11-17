"""GitBook: profile check on https://<username>.gitbook.io/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[\w@-]+?$")

SITE = Site(
    label="GitBook username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.gitbook.io/',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
