"""CyberDefenders: profile check on https://cyberdefenders.org/p/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile('^[^\\/:*?"<>|@]{3,50}$')

SITE = Site(
    label="CyberDefenders username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://cyberdefenders.org/p/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
