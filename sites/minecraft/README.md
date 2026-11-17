# findmyname - minecraft
Find available usernames on [Minecraft](https://minecraft.net/).

This tool is not fully reliable. It checks if a profile exists at `https://api.mojang.com/users/profiles/minecraft/<username>`: when the page shows a 'not found' text, the username counts as available. Reserved, banned and deleted usernames have no profile either, so it might give false positives.

This tool does not use proxies. It was tested with single requests only, limits for long runs are not known.

Valid usernames match `^.{1,25}$`.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `max_threads` start low (default 10) and raise it while there are no errors in the console.
- `max_retries` a rate limit or block page is retried this many times (3 by default) with an increasing pause. After that the username is skipped and checked again next run, it is never saved as unavailable.
