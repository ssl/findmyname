"""threads: profile check on https://www.threads.net/@<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="threads username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.threads.net/@{}',
        missing_text='<title>Threads • Log in</title>',
        headers={'Sec-Fetch-Mode': 'navigate'},
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
