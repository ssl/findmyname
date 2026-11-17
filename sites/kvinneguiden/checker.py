"""Kvinneguiden: profile check on https://forum.kvinneguiden.no/?app=core&module=system&controller=ajax&do=usernameExists&input=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]{3,18}$")

SITE = Site(
    label="Kvinneguiden username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://forum.kvinneguiden.no/?app=core&module=system&controller=ajax&do=usernameExists&input={}',
        missing_text='{"result":"ok"}',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
