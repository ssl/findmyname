import requests
from requests.structures import CaseInsensitiveDict
import sys
import os
import re
import time

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_loader import ConfigLoader
from utils.checker_utils import CheckerUtils

# Load config
config = ConfigLoader.load_config('github')

# Custom Regex for valid GitHub usernames (a-z, 0-9, hyphen, cannot start or end with hyphen)
valid_pattern = re.compile(r'^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$')

def check_github_page(username):
    """
    Check if a username is available on GitHub by checking the profile page.
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if available, False if unavailable
    """
    # Headers for requests
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    
    # GitHub profile page URL
    profile_url = f"https://gist.github.com/{username}"

    keep_trying = True
    while keep_trying:
        try:
            resp = requests.get(profile_url, headers=headers, timeout=config.get('timeout_seconds', 30))
        
            # If we get a 404 status code, the username is available
            if resp.status_code == 404:
                keep_trying = False
                return True
            
            # If we get a 200 status code, the username is taken
            if resp.status_code == 200:
                keep_trying = False
                return False
            
            # If we get a 400 status code, the username is unavailable
            if resp.status_code == 400:
                keep_trying = False
                return False
            
            # If we get a 429 status we're rate limited
            if resp.status_code == 429:
                time.sleep(10)
                raise Exception("Rate limit exceeded")
            
            # For other status codes, raise an exception
            resp.raise_for_status()
            
        except Exception as e:
            keep_trying = True

# Main Execution
if __name__ == "__main__":
    # Create a standardized check function
    check_function = CheckerUtils.create_check_function(
        check_api_function=check_github_page,
        success_condition=lambda result: result,
        success_message='[1] GitHub username {username} is available',
        error_message='Error checking GitHub username {username}: {error}'
    )
    
    # Run the checker
    CheckerUtils.run_checker(
        tool_name='github',
        script_dir=SCRIPT_DIR,
        config=config,
        check_function=check_function,
        valid_pattern=valid_pattern
    ) 