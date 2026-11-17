"""RubyGems: profile check on https://rubygems.org/profiles/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{1,40}$")

SITE = Site(
    label="RubyGems username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://rubygems.org/profiles/{}',
        missing_status=404,
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
