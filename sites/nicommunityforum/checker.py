"""NICommunityForum: profile check on https://community.native-instruments.com/profile/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="NICommunityForum username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://community.native-instruments.com/profile/{}',
        missing_text='The page you were looking for could not be found.',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
