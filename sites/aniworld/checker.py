"""AniWorld: profile check on https://aniworld.to/user/profil/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9]+$")

SITE = Site(
    label="AniWorld username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://aniworld.to/user/profil/{}',
        missing_text='Dieses Profil ist nicht verfügbar',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
