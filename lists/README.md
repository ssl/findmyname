# lists
**lists contains all kinds of potentional usernames.**

- `dutch.txt` and `english.txt` are common words.
- Every possible 1-4 character username (a-z, 0-9 and mixed) is not stored in git. Generate them into `lists/generated/` with:

```bash
python lists/generate.py
```

Use `--max-length 3` to skip the big 4 character lists.

if you looking for more, check out [SecCollection](https://github.com/ssl/SecCollection/tree/main/Wordlists)
