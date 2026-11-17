# findmyname - roblox
Find available usernames on [Roblox](https://www.roblox.com/).

This tool is reliable in results. It asks the same check the signup form uses, so reserved and inappropriate usernames are not reported as available.

This tool does not use proxies. It was tested with single requests only, limits for long runs are not known.

Valid usernames are 3-20 characters of a-z, 0-9 and at most one `_`, not at the start or end.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `max_threads` start low (default 10) and raise it while there are no errors in the console.
- `max_retries` a rate limit is retried this many times (3 by default) with an increasing pause. After that the username is skipped and checked again next run, it is never saved as unavailable.
