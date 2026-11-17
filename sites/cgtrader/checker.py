"""CGTrader: profile check on https://www.cgtrader.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[^.]*?$")

SITE = Site(
    label="CGTrader username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.cgtrader.com/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
