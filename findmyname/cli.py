"""Command line entry point: python -m findmyname <site> [usernames] [options]"""

import argparse

import colorama

from .config import load_config
from .runner import check_usernames, run
from .site import load_site, site_names

ALL = "all"

OVERRIDES = {
    "input": "input",
    "threads": "max_threads",
    "min": "min_length",
    "max": "max_length",
    "batch_size": "batch_size",
    "timeout": "timeout_seconds",
    "retries": "max_retries",
    "proxy": "proxy",
}

QUICK_DEFAULTS = {"max_retries": 1, "retry_backoff": 1}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="findmyname",
        description="Check username availability. Options override config.json.",
        epilog="examples:  python -m findmyname steam   |   python -m findmyname all john johndoe",
    )
    parser.add_argument("site", choices=site_names() + [ALL], metavar="site",
                        help=f"website to check, a folder name in sites/, or '{ALL}' for every site")
    parser.add_argument("usernames", nargs="*",
                        help="check these usernames now, instead of running through an input list")
    parser.add_argument("-i", "--input", help="username list, or a directory of lists")
    parser.add_argument("-t", "--threads", type=int, help="number of worker threads")
    parser.add_argument("--min", type=int, help="minimum username length")
    parser.add_argument("--max", type=int, help="maximum username length")
    parser.add_argument("--batch-size", type=int, help="usernames queued at a time")
    parser.add_argument("--timeout", type=float, help="request timeout in seconds")
    parser.add_argument("--retries", type=int, help="retries when a check is not certain")
    parser.add_argument("--proxy", help="proxy as user:pass@host:port")
    parser.add_argument("--config", help="path to a config file (default: config.json)")
    parser.add_argument("--data-dir", help="where results are saved (default: data/)")
    parser.add_argument("--recheck", action="store_true",
                        help="check the available usernames again and drop the ones taken by now")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    colorama.init(autoreset=True)

    overrides = {key: getattr(args, option) for option, key in OVERRIDES.items()
                 if getattr(args, option) is not None}

    if args.usernames:
        tools = load_config(None, args.config).get("tools", {})
        names = site_names() if args.site == ALL else [args.site]
        sites = []
        for name in names:
            site = load_site(name)
            sites.append((site, {**site.defaults, **QUICK_DEFAULTS, **tools.get(name, {}), **overrides}))
        _, interrupted = check_usernames(sites, args.usernames, threads=args.threads or 50)
        return 130 if interrupted else 0

    if args.site == ALL:
        parser.error(f"'{ALL}' needs one or more usernames, like: findmyname {ALL} john johndoe")

    config = {**load_config(args.site, args.config), **overrides}
    stats = run(load_site(args.site), config, data_dir=args.data_dir, recheck=args.recheck)
    return 130 if stats.interrupted else 0
