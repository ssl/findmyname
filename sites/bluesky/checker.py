"""Bluesky: profile check on https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=<username>.bsky.social"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,16}[a-z0-9]$")

SITE = Site(
    label="Bluesky username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={}.bsky.social',
        missing_status=400,
        missing_text='Unable to resolve handle',
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
