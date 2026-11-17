"""AWS Skills Profile: profile check on https://skillsprofile.skillbuilder.aws/user/<username>/"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="AWS Skills Profile username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://skillsprofile.skillbuilder.aws/user/{}/',
        missing_text='shareProfileAccepted":false',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
