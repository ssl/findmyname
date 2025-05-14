# findmyname

**Check username availability on various websites including:**
- Instagram
- Steam
- GitHub

The findmyname project includes a set of username checkers, each in its own directory with a dedicated README. All tools use shared utilities, ensuring consistent functionality and making it easy to add new websites. Some leverage proxies while others implement smart techniques to bypass rate limits.

## Configuration

Set up all tools with one `config.json` file in the main directory.

1. Copy the example config:
   ```bash
   cp example.config.json config.json
   ```
2. Edit `config.json` with tool-specific details.

Defaults are used if no config is provided.

## Usage

Each tool has its own `README.md` with full details. Run a tool like this:

```bash
# Example for Steam
python steam/checker.py
```

## Input Processing

Input files are cleaned up by removing:
- Invalid usernames per site rules
- Previously checked usernames
- Usernames too short or long per config
- Duplicates

## Output

Results save to `data/`. Console shows progress, like:

```
Progress: 251/27535 (0.91%) | TA: 560 | TU: 29978 | Speed: 50.06 names/sec | ETA: 9m 5s
[1] GitHub username ssl is available
```