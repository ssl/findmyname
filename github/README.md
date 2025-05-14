# findmyname - github
Find available usernames on github.

This tool is not fully reliable. It might give false positives (mostly in reserved or bad words). It won't give false negatives.

This one does not use proxies and uses GitHub's avatars API to check if the avatar file hash is equal to the 'not found' avatar.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `min_length` recommend at 3 atleast.
- `max_threads` whatever you can handle. recommend around 50 to be nice to github
