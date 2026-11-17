"""SpaceHey: profile check on https://spacehey.com/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="SpaceHey username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://spacehey.com/{}',
        missing_text='Not Found (Error 404) | SpaceHey',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
