import requests
from requests.structures import CaseInsensitiveDict
import sys
import os
import re
import time
import hashlib

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_loader import ConfigLoader
from utils.checker_utils import CheckerUtils

# Load config
config = ConfigLoader.load_config('github')

# Custom Regex for valid GitHub usernames (a-z, 0-9, hyphen, cannot start or end with hyphen)
# valid_pattern = re.compile(r'^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$')
valid_pattern = re.compile(r'^[a-z0-9]{0,3}$')

def check_github_page(username):
    """
    Check if a username is available on GitHub by checking the avatar image.
    If the avatar is the same as the default avatar, the username is available.
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if available, False if unavailable
    """
    # Headers for requests
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    
    # GitHub avatar URL
    avatar_url = f"https://avatars.githubusercontent.com/{username}?s=1"

    keep_trying = True
    while keep_trying:
        try:
            resp = requests.get(avatar_url, headers=headers, timeout=10)
            
            # If we get a 200 status code, check if the avatar is the default one
            if resp.status_code == 200:
                keep_trying = False
                # Calculate hash of the response content
                avatar_hash = hashlib.md5(resp.content).hexdigest()
                # If the hash matches the default avatar, the username is available
                return avatar_hash == '2785b1bedaed3962692a1850a4c50faa'
            
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