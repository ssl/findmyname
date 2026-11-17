"""Reading input lists and reading/writing result files."""

import os
import re
from pathlib import Path

from colorama import Fore

from . import REPO_ROOT

ENCODINGS = ("utf-8", "latin-1")
SKIPPED_SUFFIXES = (".md", ".py", ".json")
DEFAULT_PATTERN = re.compile(r"^[a-z0-9.]+$")


def resolve_input_path(input_path):
    """Relative paths are tried against the working directory, then the repository root."""
    path = Path(input_path).expanduser()
    if path.is_absolute() or path.exists():
        return path
    return REPO_ROOT / path


def read_lines(file_path):
    """Read all lines of one file, trying several encodings."""
    last_error = None
    for encoding in ENCODINGS:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.readlines()
        except UnicodeDecodeError as e:
            last_error = e
        except OSError as e:
            last_error = e
            break

    print(Fore.RED + f"Could not read {file_path}: {last_error}")
    return []


def read_input(input_path):
    """Read all lines from an input file, or from every list in a directory."""
    path = Path(input_path)

    if path.is_dir():
        lines = []
        for root, dirs, files in os.walk(path):
            dirs[:] = sorted(d for d in dirs if not d.startswith((".", "__")))
            for filename in sorted(files):
                if filename.startswith(".") or filename.lower().endswith(SKIPPED_SUFFIXES):
                    continue
                lines.extend(read_lines(os.path.join(root, filename)))
        return lines

    if not path.exists():
        print(Fore.RED + f"Input not found: {path}")
        return []

    return read_lines(path)


def filter_usernames(usernames, min_length=1, max_length=50, valid_pattern=None):
    """Lowercase, deduplicate and drop usernames that are invalid or out of range."""
    if valid_pattern is None:
        valid_pattern = DEFAULT_PATTERN

    seen = set()
    filtered = []
    for username in usernames:
        username = username.strip().lower()
        if (
            username
            and username not in seen
            and min_length <= len(username) <= max_length
            and valid_pattern.match(username)
        ):
            seen.add(username)
            filtered.append(username)
    return filtered


def result_paths(tool_name, data_dir):
    """Create the data directory and return (available, unavailable, sorted) paths."""
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    available = data_dir / f"{tool_name}_available.txt"
    unavailable = data_dir / f"{tool_name}_unavailable.txt"
    sorted_available = data_dir / f"{tool_name}_sorted_available.txt"

    for path in (available, unavailable):
        path.touch(exist_ok=True)

    return available, unavailable, sorted_available


def load_names(path):
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def rewrite_without(path, removed):
    """Rewrite a result file without the given usernames."""
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(path, "r", encoding="utf-8") as src, open(tmp, "w", encoding="utf-8") as dst:
        for line in src:
            name = line.strip()
            if name and name.lower() not in removed:
                dst.write(f"{name}\n")
    os.replace(tmp, path)


def sort_and_save(available_file, sorted_file):
    """Write the available usernames sorted by length, then alphabetically."""
    with open(available_file, "r", encoding="utf-8") as f:
        names = {line.strip() for line in f if line.strip()}

    ordered = sorted(names, key=lambda name: (len(name), name))
    with open(sorted_file, "w", encoding="utf-8") as f:
        for name in ordered:
            f.write(f"{name}\n")

    print(Fore.GREEN + f"Sorted {len(ordered)} available usernames saved to {sorted_file}")
