import requests
from requests.structures import CaseInsensitiveDict
import sys
import os
import re

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_loader import ConfigLoader
from utils.checker_utils import CheckerUtils

# Load config
config = ConfigLoader.load_config('steam')

# Custom Regex for valid usernames (a-z, 0-9, .)
valid_pattern = re.compile(r'^[a-z0-9.]+$')

def check_steam_api(username):
    """
    Check if a username is available on Steam via API.
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if available, False if unavailable
    """
    # Headers for requests
    headers = CaseInsensitiveDict()
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"

    user_url = "https://steamcommunity.com/id/" + username

    resp = requests.get(user_url, headers=headers, timeout=config.get('timeout_seconds', 30))
    return "<title>Steam Community :: Error</title>" in resp.text

# Main Execution
if __name__ == "__main__":
    # Create a standardized check function
    check_function = CheckerUtils.create_check_function(
        check_api_function=check_steam_api,
        success_condition=lambda result: result,
        success_message='[1] Username {username} is available',
        error_message='Error checking {username}: {error}'
    )
    
    # Run the checker
    CheckerUtils.run_checker(
        tool_name='steam',
        script_dir=SCRIPT_DIR,
        config=config,
        check_function=check_function,
        valid_pattern=valid_pattern
    )