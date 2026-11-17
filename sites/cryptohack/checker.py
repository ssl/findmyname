"""CryptoHack: profile check on https://cryptohack.org/user/<username>/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="CryptoHack username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://cryptohack.org/user/{}/',
        missing_redirect=True,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
