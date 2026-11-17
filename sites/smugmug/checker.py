"""SmugMug: profile check on https://<username>.smugmug.com"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z]{1,35}$")

SITE = Site(
    label="SmugMug username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.smugmug.com',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
