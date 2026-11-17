"""NitroType: profile check on https://www.nitrotype.com/racer/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="NitroType username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://www.nitrotype.com/racer/{}',
        missing_text='<title>Nitro Type | Competitive Typing Game | Race Your Friends</title>',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
