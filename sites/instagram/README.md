# findmyname - instagram
Find available usernames on instagram.

This tool is 100% reliable in results.

Just run it, if your proxies are working and your config is correct take a coffee and grab your usernames.

Important: the tool tries to get a new proxy connection if the result is not certain, up to `max_retries` times per username (25 by default). If your proxy pool is limited or LQ, and all are ratelimited or banned, those retries still use proxy data. If this happens, you will clearly see errors in the console and no growing results. Usernames that ran out of retries are checked again next run.

## Config

- `input` can be an text file with a new username on every line, or a directory containing these files.
- `min_length` recommend atleast 5. It seems no 4 char or shorter is still available (yes, I checked) - or instagram is not allowing them to register no more.
- `max_retries` how often an uncertain result is tried again with a new proxy connection.
- `max_threads` with HQ proxies this is mostly about what can your PC handle?

## Proxy Management
High-quality, preferable residential proxies are needed to bypass ratelimits. 1 GB gives about 100.000 username checks.

For best results, use a proxy with a single connection, that provides a new IP on every connection. If you want to use a proxy list to rotate instead, edit the `get_random_proxy()` function in `checker.py`.

Some cheap options;
- https://www.lunaproxy.com/pricing/rotating-isp-proxies/
- https://dataimpulse.com
