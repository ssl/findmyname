"""LiveJournal: profile check on https://<username>.livejournal.com"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

SITE = Site(
    label="LiveJournal username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.livejournal.com',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
