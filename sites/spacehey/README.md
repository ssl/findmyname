# findmyname - spacehey
Find available usernames on [SpaceHey](https://spacehey.com/).

This tool is not fully reliable. It checks if a profile exists at `https://spacehey.com/<username>`: when the page shows a 'not found' text, the username counts as available. Reserved, banned and deleted usernames have no profile either, so it might give false positives.

This tool does not use proxies. It was tested with single requests only, limits for long runs are not known.

The username rules of SpaceHey are not known, so only a-z and 0-9 are checked. Edit `VALID_PATTERN` in `checker.py` if more is allowed.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `max_threads` start low (default 10) and raise it while there are no errors in the console.
- `max_retries` a rate limit or block page is retried this many times (3 by default) with an increasing pause. After that the username is skipped and checked again next run, it is never saved as unavailable.
