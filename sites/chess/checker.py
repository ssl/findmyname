"""Chess: profile check on https://www.chess.com/callback/user/valid?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,25}$")

SITE = Site(
    label="Chess username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.chess.com/callback/user/valid?username={}',
        missing_text='Username is valid',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
