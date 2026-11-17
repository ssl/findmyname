"""The shared run loop: filter input, check with a thread pool, save results."""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from colorama import Fore

from . import REPO_ROOT, files
from .site import RetryableError

AVAILABLE, TAKEN, ERROR, SKIPPED = "available", "taken", "error", "skipped"

PROGRESS_INTERVAL = 5
MAX_BACKOFF = 60


@dataclass
class Stats:
    total: int = 0
    available: int = 0
    taken: int = 0
    errors: int = 0
    interrupted: bool = False

    @property
    def checked(self):
        return self.available + self.taken + self.errors


def check_with_retries(site, username, config, stop):
    """Check one username, retrying uncertain answers."""
    max_retries = int(config.get("max_retries", 5))
    backoff = float(config.get("retry_backoff", 1))
    last_error = None

    for attempt in range(max_retries + 1):
        if stop.is_set():
            return SKIPPED, None
        try:
            return (AVAILABLE if site.check(username, config) else TAKEN), None
        except RetryableError as e:
            last_error = e
            if attempt < max_retries and backoff > 0:
                stop.wait(min(backoff * 2 ** attempt, MAX_BACKOFF))
        except Exception as e:
            return ERROR, e

    return ERROR, last_error


def _format_eta(seconds):
    seconds = int(seconds)
    if seconds >= 3600:
        return f"{seconds // 3600}h {seconds % 3600 // 60}m"
    return f"{seconds // 60}m {seconds % 60}s"


def run(site, config, data_dir=None, recheck=False):
    """Run a site checker and return the Stats of this run."""
    config = {**site.defaults, **config}
    data_dir = data_dir or REPO_ROOT / "data"

    threads = int(config.get("max_threads", 10))
    batch_size = max(int(config.get("batch_size", 1000)), 1)
    min_length = int(config.get("min_length", 1))
    max_length = int(config.get("max_length", 50))

    available_file, unavailable_file, sorted_file = files.result_paths(site.name, data_dir)
    available_set = files.load_names(available_file)
    unavailable_set = files.load_names(unavailable_file)

    if recheck:
        usernames = files.filter_usernames(sorted(available_set), 1, 10**6, site.pattern)
        print(Fore.BLUE + f"Rechecking {len(usernames)} available usernames")
    else:
        input_path = files.resolve_input_path(config.get("input", REPO_ROOT / "lists"))
        lines = files.read_input(input_path)
        print(Fore.BLUE + f"Original count: {len(lines)}")

        usernames = files.filter_usernames(lines, min_length, max_length, site.pattern)
        usernames = [u for u in usernames if u not in available_set and u not in unavailable_set]
        print(Fore.BLUE + f"Filtered count: {len(usernames)}")

    stats = Stats(total=len(usernames))
    if not usernames:
        print(Fore.GREEN + "No new usernames to check.")
        files.sort_and_save(available_file, sorted_file)
        return stats

    print(Fore.BLUE + f"Processing {stats.total} usernames with {threads} threads")

    lock = threading.Lock()
    stop = threading.Event()
    done = threading.Event()
    start_time = time.time()
    newly_taken = set()
    base_available = len(available_set)
    base_unavailable = len(unavailable_set)

    def progress_line():
        with lock:
            checked, found, taken, errors = stats.checked, stats.available, stats.taken, stats.errors
        elapsed = time.time() - start_time
        speed = checked / elapsed if elapsed > 0 else 0
        eta = _format_eta((stats.total - checked) / speed) if speed > 0 else "?"
        if recheck:
            total_available, total_unavailable = base_available - taken, base_unavailable + taken
        else:
            total_available, total_unavailable = base_available + found, base_unavailable + taken
        line = (f"Progress: {checked}/{stats.total} ({checked / stats.total * 100:.2f}%) | "
                f"TA: {total_available} | TU: {total_unavailable} | ")
        if errors:
            line += f"Errors: {errors} | "
        return line + f"Speed: {speed:.2f} names/sec | ETA: {eta}"

    def monitor():
        while not done.wait(PROGRESS_INTERVAL):
            print(Fore.CYAN + progress_line())

    available_out = open(available_file, "a", encoding="utf-8", buffering=1)
    unavailable_out = open(unavailable_file, "a", encoding="utf-8", buffering=1)

    def worker(username):
        outcome, error = check_with_retries(site, username, config, stop)
        with lock:
            if outcome == AVAILABLE:
                stats.available += 1
                if not recheck:
                    available_out.write(f"{username}\n")
            elif outcome == TAKEN:
                stats.taken += 1
                unavailable_out.write(f"{username}\n")
                newly_taken.add(username)
            elif outcome == ERROR:
                stats.errors += 1
        if outcome == AVAILABLE and not recheck:
            print(Fore.GREEN + f"[1] {site.label} {username} is available")
        elif outcome == TAKEN and recheck:
            print(Fore.YELLOW + f"[0] {site.label} {username} is no longer available")
        elif outcome == ERROR:
            print(Fore.RED + f"Error checking {site.label} {username}: {error}")

    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()

    executor = ThreadPoolExecutor(max_workers=threads)
    try:
        for i in range(0, stats.total, batch_size):
            futures = [executor.submit(worker, u) for u in usernames[i:i + batch_size]]
            for future in as_completed(futures):
                future.result()
    except KeyboardInterrupt:
        stats.interrupted = True
        stop.set()
        print(Fore.YELLOW + "\nInterrupted, waiting for running checks to finish...")
        executor.shutdown(wait=True, cancel_futures=True)
    finally:
        stop.set()
        executor.shutdown(wait=True, cancel_futures=True)
        done.set()
        monitor_thread.join()
        available_out.close()
        unavailable_out.close()

    print(Fore.CYAN + progress_line())

    if recheck and newly_taken:
        files.rewrite_without(available_file, newly_taken)
    files.sort_and_save(available_file, sorted_file)

    if stats.errors:
        print(Fore.YELLOW + f"{stats.errors} usernames gave no certain answer and will be checked again next run.")
    if stats.interrupted:
        print(Fore.YELLOW + f"{site.name.capitalize()} username check stopped early; run again to continue.")
    else:
        print(Fore.GREEN + f"{site.name.capitalize()} username check completed!")

    return stats


INVALID = "invalid"


def check_usernames(sites, usernames, threads=50):
    """Check a few usernames directly on one or more sites."""
    usernames = list(dict.fromkeys(u.strip().lower() for u in usernames if u.strip()))
    results = {u: {AVAILABLE: [], TAKEN: [], INVALID: [], ERROR: []} for u in usernames}
    stop = threading.Event()
    lock = threading.Lock()

    def worker(site, config, username):
        outcome, _ = check_with_retries(site, username, config, stop)
        if outcome == AVAILABLE and len(sites) > 1:
            print(Fore.GREEN + f"[1] {site.label} {username} is available")
        if outcome != SKIPPED:
            with lock:
                results[username][outcome].append(site.name)

    jobs = []
    for site, config in sites:
        for username in usernames:
            if site.pattern.match(username):
                jobs.append((site, {**site.defaults, **config}, username))
            else:
                results[username][INVALID].append(site.name)

    print(Fore.BLUE + f"Checking {len(usernames)} username{'s' * (len(usernames) != 1)} "
                      f"on {len(sites)} site{'s' * (len(sites) != 1)}")

    executor = ThreadPoolExecutor(max_workers=threads)
    interrupted = False
    try:
        for future in as_completed([executor.submit(worker, *job) for job in jobs]):
            future.result()
    except KeyboardInterrupt:
        interrupted = True
        print(Fore.YELLOW + "\nInterrupted, waiting for running checks to finish...")
    finally:
        stop.set()
        executor.shutdown(wait=True, cancel_futures=True)

    rows = [
        (AVAILABLE, Fore.GREEN, "available"),
        (TAKEN, Fore.RED, "taken"),
        (INVALID, Fore.YELLOW, "not a valid username there"),
        (ERROR, Fore.YELLOW, "no certain answer"),
    ]
    for username in usernames:
        print()
        print(Fore.CYAN + username)
        for outcome, color, text in rows:
            names = sorted(results[username][outcome])
            if names:
                print(color + f"  {text} ({len(names)}): " + ", ".join(names))

    return results, interrupted
