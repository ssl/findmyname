# findmyname - rajce_net
Find available usernames on [Rajce.net](https://www.rajce.idnes.cz/).

This tool is not fully reliable. It checks if a profile exists at `https://<username>.rajce.idnes.cz/`: when the page gives HTTP 410, the username counts as available. Reserved, banned and deleted usernames have no profile either, so it might give false positives.

This tool does not use proxies. It was tested with single requests only, limits for long runs are not known.

Valid usernames match `^[\w@-]+?$`.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `max_threads` start low (default 10) and raise it while there are no errors in the console.
- `max_retries` a rate limit or block page is retried this many times (3 by default) with an increasing pause. After that the username is skipped and checked again next run, it is never saved as unavailable.
