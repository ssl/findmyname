# findmyname - discord
Find available usernames on [Discord](https://discord.com/).

This tool is reliable in results. It asks the same check the signup form uses. Usernames Discord does not allow at all are saved as unavailable.

This tool does not use proxies. Discord limits this check strictly, so it is slow: expect rate limits after a handful of requests. It was tested with single requests only.

Valid usernames are 2-32 characters of a-z, 0-9, `_` and `.`, without two dots in a row.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `max_threads` 2 by default. Higher only gives more rate limits.
- `max_retries` a rate limit is retried this many times (5 by default) with an increasing pause. After that the username is skipped and checked again next run, it is never saved as unavailable.
