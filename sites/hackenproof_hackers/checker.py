"""HackenProof (Hackers): profile check on https://hackenproof.com/hackers/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[\w-]{,34}$")

SITE = Site(
    label="HackenProof (Hackers) username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://hackenproof.com/hackers/{}',
        missing_text='Page not found',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
