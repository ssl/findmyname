# findmyname - steam
Find available usernames on steam.

This tool is not fully reliable. It might give false positives (mostly in 1-3 char usernames or bad words). It won't give false negatives.

This tool does not need proxies as profile visits are not heavily limited. It is recommended however to not put threads too high.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `min_length` recommend at 3 or 4 atleast.
- `max_threads` since no proxies are used, don't put it too high.
- `timeout_seconds` request timeout, 30 by default.
- `max_retries` a rate limit or server error is retried this many times (3 by default) with an increasing pause. After that the username is skipped and checked again next run, it is never saved as unavailable.

Valid usernames contain a-z, 0-9, `_` and `-`.

