"""Minecraft: profile check on https://api.mojang.com/users/profiles/minecraft/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^.{1,25}$")

SITE = Site(
    label="Minecraft username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://api.mojang.com/users/profiles/minecraft/{}',
        missing_text="Couldn't find any profile with name",
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
