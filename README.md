# findmyname
findmyname is a collection of username checkers for various sites

## Supported sites

### Instagram
### Steam
### GitHub

## Configuration

This project uses a centralized configuration system that allows all tools to access their specific configuration values from a single `config.json` file in the main directory.

To start, copy `example.config.json` to `config.json` and fill in the config details
```bash
cp example.config.json config.json
```

## Running the Tools

All tools have their own `README.md` in the directory, with detailed description about the specific tool.

To run a tool, simply execute its checker.py file. Example;

```bash
# For the Steam tool
python steam/checker.py
```

Input files are automatically stripped of;
- If invalid per site rules
- If already checked (available/unavailable from previous runs)
- If too short/long from config file
- Dublicates in file

## Output
All checked usernames are in the data/ folder