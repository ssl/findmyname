"""Wikipedia: profile check on https://en.wikipedia.org/wiki/Special:CentralAuth/<username>?uselang=qqx"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="Wikipedia username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://en.wikipedia.org/wiki/Special:CentralAuth/{}?uselang=qqx',
        missing_text='centralauth-admin-nonexistent:',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
