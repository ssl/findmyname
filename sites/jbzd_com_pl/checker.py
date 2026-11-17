"""jbzd.com.pl: profile check on https://jbzd.com.pl/uzytkownik/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="jbzd.com.pl username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://jbzd.com.pl/uzytkownik/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
