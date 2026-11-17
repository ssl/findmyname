# findmyname - hacker_news
Find available usernames on [Hacker News](https://news.ycombinator.com/).

This tool is not fully reliable. It asks the public API if a user exists. Usernames are case sensitive on Hacker News and this tool only checks lowercase, and users without any activity are not in the API, so it might give false positives.

This tool does not use proxies. It was tested with single requests only, limits for long runs are not known.

Valid usernames are 2-15 characters of a-z, 0-9, `_` and `-`.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `max_threads` start low (default 10) and raise it while there are no errors in the console.
- `max_retries` a failed request is retried this many times (3 by default) with an increasing pause. After that the username is skipped and checked again next run.
