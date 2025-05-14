#!/usr/bin/env python3
"""
Generate lists of potential usernames with different lengths and character sets.
This script creates 18 different lists:
- 6 lengths (1-6 characters)
- 3 character sets (a-z, 0-9, and mixed a-z0-9)
"""

import os
import itertools
import string
from pathlib import Path

# Define character sets
LOWERCASE = string.ascii_lowercase  # a-z
DIGITS = string.digits  # 0-9
MIXED = LOWERCASE + DIGITS  # a-z0-9

# Define output directory
OUTPUT_DIR = Path(__file__).parent / "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_combinations(char_set, length):
    """Generate all possible combinations of characters from the given set with the specified length."""
    return [''.join(combo) for combo in itertools.product(char_set, repeat=length)]

def save_to_file(items, filename):
    """Save the generated items to a file."""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w') as f:
        for item in items:
            f.write(f"{item}\n")
    print(f"Generated {len(items)} items in {filepath}")

def main():
    # Generate lists for each length (1-4) and character set (a-z, 0-9, mixed)
    for length in range(1, 5):
        # Generate a-z lists
        lowercase_items = generate_combinations(LOWERCASE, length)
        save_to_file(lowercase_items, f"a-z_{length}char.txt")
        
        # Generate 0-9 lists
        digit_items = generate_combinations(DIGITS, length)
        save_to_file(digit_items, f"0-9_{length}char.txt")
        
        # Generate mixed a-z0-9 lists
        mixed_items = generate_combinations(MIXED, length)
        save_to_file(mixed_items, f"mixed_{length}char.txt")
    
    print(f"All lists have been generated in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
