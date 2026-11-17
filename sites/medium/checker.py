"""Medium: profile check on https://medium.com/feed/@<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Medium username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://medium.com/feed/@{}',
        missing_text='<body',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
