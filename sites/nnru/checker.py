"""nnRU: profile check on https://<username>.www.nn.ru/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[\w@-]+?$")

SITE = Site(
    label="nnRU username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://{}.www.nn.ru/',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
