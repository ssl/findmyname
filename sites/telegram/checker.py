"""Telegram: profile check on https://t.me/<username>"""

import re

from findmyname.profile import profile_check
from findmyname.site import Site

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,32}[^_]$")

SITE = Site(
    label="Telegram username",
    pattern=VALID_PATTERN,
    check=profile_check(
        url='https://t.me/{}',
        missing_text=(
            '<title>Telegram Messenger</title>',
            'If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link" href="tg://resolve?domain=',
        ),
    ),
    defaults={"max_retries": 3, "retry_backoff": 5},
)
