"""TrashboxRU: profile check on https://trashbox.ru/users/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,16}$")

SITE = Site(
    label="TrashboxRU username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://trashbox.ru/users/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
