# findmyname

**Check username availability on 200+ websites**, including Instagram, Steam, GitHub, Roblox, Discord, X, Telegram and YouTube.

Run a whole wordlist against one site, or check one username on every site at once.

## Install

```bash
pip install -r requirements.txt
```

## Usage

Run a list of usernames against one site:

```bash
python -m findmyname steam
python -m findmyname github --input lists/english.txt --min 3 --max 5 --threads 50
```

Check one or a few usernames right away, on one site or on `all` of them:

```bash
python -m findmyname all johndoe
python -m findmyname telegram johndoe john.doe
```

Check the saved available usernames again and drop the ones taken by now:

```bash
python -m findmyname steam --recheck
```

Stop a run with Ctrl+C. The next run continues where it stopped.

## Configuration

Copy `example.config.json` to `config.json` and edit it. Without a config, defaults are used. Command line options override the config.

| Config key | Option | Default | Meaning |
| --- | --- | --- | --- |
| `input` | `-i`, `--input` | `lists/` | A text file with one username per line, or a directory of such files |
| `max_threads` | `-t`, `--threads` | 10 | Number of worker threads |
| `min_length` | `--min` | 1 | Shortest username to check |
| `max_length` | `--max` | 50 | Longest username to check |
| `batch_size` | `--batch-size` | 1000 | Usernames queued at a time |
| `timeout_seconds` | `--timeout` | per site | Request timeout |
| `max_retries` | `--retries` | per site | Retries when a check gives no certain answer |
| `retry_backoff` | | per site | Seconds before the first retry, doubling every retry |
| `proxy` | `--proxy` | none | Instagram only, as `user:pass@host:port` |

## Input and output

Input is cleaned up first: invalid usernames for the site, duplicates, usernames outside the length range and usernames that were already checked are removed. See [lists](lists/) for the included lists.

Results save to `data/`:
- `<site>_available.txt` in the order they were found
- `<site>_sorted_available.txt` sorted by length, then alphabetically
- `<site>_unavailable.txt` so they are not checked again

A username that keeps giving no certain answer is saved to neither file and is checked again next run. Checks of usernames given on the command line are not saved.

```
Progress: 251/27535 (0.91%) | TA: 560 | TU: 29978 | Speed: 50.06 names/sec | ETA: 9m 5s
[1] GitHub username ssl is available
```

## Sites

Every site has its own folder in [sites](sites/) with a `checker.py` and a `README.md` about its reliability and limits. The folder name is the name used on the command line.

There are two kinds:
- **Signup checks** ask the site if a username can be registered, like [Instagram](sites/instagram/), [Roblox](sites/roblox/) and [Discord](sites/discord/). These are reliable.
- **Profile checks** look if a profile exists. A username without a profile can still be reserved, banned or deleted, so these might give false positives.

## Adding a website

Add a folder to `sites/` with a `checker.py` and a `README.md`. Nothing else needs to be registered.

`checker.py` defines `SITE = Site(...)` with a regex for valid usernames and a `check(username, config)` function. It returns `True` when the username is available, `False` when it is taken, and raises `RetryableError` when the answer is not certain. See [steam](sites/steam/checker.py) for a custom check, or [chess](sites/chess/checker.py) for a profile check.
