import requests
import json
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
config = ConfigLoader.load_config('instagram')

# Custom Regex for valid usernames (a-z, 0-9, .)
valid_pattern = re.compile(r'^(?!\.)(?!.*\.\.)(?!.*^\d+$)[a-z0-9.]+(?<!\.)$')

# Proxy Management
def get_random_proxy():
    proxy = config.get('proxy', '')
    return proxy

# Checking Methods
def check_instagram_api(username):
    """
    Check if a username is available on Instagram via API.
    
    Args:
        username (str): Username to check
        
    Returns:
        int: 1 if available, 0 if unavailable
    """
    url = "https://www.instagram.com:443/accounts/web_create_ajax/attempt/"
    headers = {
        "X-Ig-Www-Claim": "0", "X-Instagram-Ajax": "ee0117db2fab",
        "Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest", "X-Asbd-Id": "198387",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "X-Csrftoken": "POttsFJopRtOI0HqAqrcZDXq6nX6haa2", "X-Ig-App-Id": "936619743392459",
        "Sec-Gpc": "1", "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty", "Referer": "https://www.instagram.com/accounts/emailsignup/",
        "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en;q=0.9",
        "Connection": "close"
    }
    data = {"email": '', "username": username, "first_name": '', "opt_into_one_tap": "false"}
    
    keep_trying = True
    while keep_trying:
        proxy = get_random_proxy()
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        
        try:
            response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=10)
            if 'Try again later' in response.text:
                raise Exception("Proxy is rate limited")
            json_response = json.loads(response.content.decode('utf8'))
            if json_response.get('errors', {}).get('email') is not None:
                keep_trying = False
                return 1 if json_response.get('errors', {}).get('username') is None else 0  # 1: Available, 0: Unavailable
            
            raise Exception("Proxy blocked")
        except Exception as e:
            keep_trying = True

# Main Execution
if __name__ == "__main__":
    # Create a standardized check function
    check_function = CheckerUtils.create_check_function(
        check_api_function=check_instagram_api,
        success_condition=lambda result: result == 1,
        success_message='[1] User {username} is available',
        error_message='Error checking {username}: {error}'
    )
    
    # Run the checker
    CheckerUtils.run_checker(
        tool_name='instagram',
        script_dir=SCRIPT_DIR,
        config=config,
        check_function=check_function,
        valid_pattern=valid_pattern
    )