"""HudsonRock: profile check on https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username=<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="HudsonRock username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={}',
        missing_text='This username is not associated',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
