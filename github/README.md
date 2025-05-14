# findmyname - github
Find available usernames on github.

This tool is not fully reliable. It might give false positives (mostly in reserved or bad words). It won't give false negatives.

This one does not use proxies and respects GitHub's ratelimits. Because GitHub is our friend.

With a maximum of 1-5 threads, ratelimit will not/rarely be hit and gives about 2-10 usernames/sec

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `min_length` recommend at 3 atleast.
- `max_threads` since no proxies are used, don't put it too high. recommended at 4

