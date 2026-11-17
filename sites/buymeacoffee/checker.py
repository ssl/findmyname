"""BuyMeACoffee: profile check on https://www.buymeacoffee.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9]{3,15}$")

SITE = Site(
    label="BuyMeACoffee username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.buymeacoffee.com/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
