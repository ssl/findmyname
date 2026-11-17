"""Generate every possible username of a given length."""

import argparse
import itertools
import string
from pathlib import Path

CHARSETS = {
    "a-z": string.ascii_lowercase,
    "0-9": string.digits,
    "mixed": string.ascii_lowercase + string.digits,
}


def generate(out_dir, max_length=4):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    groups = [("1-2char", (1, 2))] + [(f"{n}char", (n,)) for n in range(3, max_length + 1)]

    for charset_name, chars in CHARSETS.items():
        for group_name, lengths in groups:
            if min(lengths) > max_length:
                continue
            path = out_dir / f"{charset_name}_{group_name}.txt"
            count = 0
            with open(path, "w", encoding="utf-8") as f:
                for length in lengths:
                    if length > max_length:
                        continue
                    for combo in itertools.product(chars, repeat=length):
                        f.write("".join(combo) + "\n")
                        count += 1
            print(f"{path}: {count} usernames")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate short username lists.")
    parser.add_argument("--max-length", type=int, default=4, help="longest username to generate (default: 4)")
    parser.add_argument("--out", default=Path(__file__).resolve().parent / "generated", help="output directory")
    args = parser.parse_args()
    generate(args.out, args.max_length)
