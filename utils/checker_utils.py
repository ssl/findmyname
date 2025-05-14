import os
import time
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore
from .file_utils import FileUtils

class CheckerUtils:
    """Utility class for checker operations shared across all checkers."""
    
    @staticmethod
    def run_checker(tool_name, script_dir, config, check_function, valid_pattern=None, min_length=None, max_length=None):
        """
        Run a checker with the given configuration and check function.
        
        Args:
            tool_name (str): Name of the tool (e.g., 'instagram', 'steam')
            script_dir (str): Directory where the script is located
            config (dict): Configuration for the tool
            check_function (callable): Function to check a username
            valid_pattern (re.Pattern, optional): Regex pattern for valid usernames
            min_length (int, optional): Minimum username length (defaults to config value)
            max_length (int, optional): Maximum username length (defaults to config value)
            
        Returns:
            None
        """
        # Get configuration values
        repo_root = os.path.dirname(script_dir)
        default_input = os.path.join(repo_root, 'lists/')

        input_list = config.get('input', default_input)
        input_threads = config.get('max_threads', 10)
        batch_size = config.get('batch_size', 1000)
        
        # Use provided values or defaults from config
        if min_length is None:
            min_length = config.get('min_length', 1)
        if max_length is None:
            max_length = config.get('max_length', 50)
        
        # Set up data directory and files
        data_dir, available_file, unavailable_file, sorted_available_file = FileUtils.setup_data_directory(tool_name, script_dir)
        
        # Create locks for thread-safe writing
        available_lock = threading.Lock()
        unavailable_lock = threading.Lock()
        progress_lock = threading.Lock()
        
        # Load existing checked usernames
        available_set, unavailable_set = FileUtils.load_existing_results(available_file, unavailable_file)
        
        # Load input usernames
        all_lines = FileUtils.get_all_lines_from_input(input_list, script_dir)
        
        # Original count
        print(Fore.BLUE + f"Original count: {len(all_lines)}")
        
        # Filter usernames
        usernames = FileUtils.filter_usernames(all_lines, min_length, max_length, valid_pattern)
        
        # Remove already checked usernames
        already_checked = available_set.union(unavailable_set)
        usernames = [u for u in usernames if u not in already_checked]
        
        print(Fore.BLUE + f"Filtered count: {len(usernames)}")
        
        if len(usernames) == 0:
            print(Fore.GREEN + "No new usernames to check.")
            FileUtils.sort_and_save_results(available_file, sorted_available_file)
            return
        
        # Process in batches
        batches = [usernames[i:i + batch_size] for i in range(0, len(usernames), batch_size)]
        total_batches = len(batches)
        print(Fore.BLUE + f"Total batches: {total_batches}")
        
        # Calculate total usernames for this run
        total_usernames = len(usernames)
        
        # Create progress file
        progress_file, timestamp = FileUtils.create_progress_file()
        
        # Start progress monitor
        start_time = time.time()
        progress_thread = FileUtils.create_progress_monitor(progress_file, total_usernames, start_time, available_file, unavailable_file)
        
        # Process all usernames
        print(Fore.BLUE + f"Processing {total_usernames} usernames with {input_threads} threads")
        
        # Create a wrapper function that includes the locks and file paths
        def check_wrapper(username):
            return check_function(
                username, 
                progress_file, 
                available_file, 
                unavailable_file, 
                available_lock, 
                unavailable_lock, 
                progress_lock
            )
        
        with ThreadPoolExecutor(max_workers=input_threads) as executor:
            futures = {executor.submit(check_wrapper, username): username 
                       for username in usernames}
            for future in as_completed(futures):
                username = futures[future]
                try:
                    result = future.result()
                except Exception as e:
                    print(Fore.RED + f"Error processing {username}: {e}")
        
        # Wait for progress monitor to finish
        progress_thread.join()
        
        # Sort available usernames
        FileUtils.sort_and_save_results(available_file, sorted_available_file)
        
        # Delete progress file
        os.remove(progress_file)
        
        print(Fore.GREEN + f"{tool_name.capitalize()} username check completed!")
    
    @staticmethod
    def create_check_function(check_api_function, success_condition, success_message, error_message=None):
        """
        Create a standardized check function for a tool.
        
        Args:
            check_api_function (callable): Function that checks a username via API
            success_condition (callable): Function that determines if the check was successful
            success_message (str): Message to print when a username is available
            error_message (str, optional): Message to print when an error occurs
            
        Returns:
            callable: A standardized check function
        """
        def check_function(username, progress_file, available_file, unavailable_file, 
                          available_lock, unavailable_lock, progress_lock):
            """
            Standardized check function for a tool.
            
            Args:
                username (str): Username to check
                progress_file (str): Path to progress file
                available_file (str): Path to available file
                unavailable_file (str): Path to unavailable file
                available_lock (threading.Lock): Lock for available file
                unavailable_lock (threading.Lock): Lock for unavailable file
                progress_lock (threading.Lock): Lock for progress file
                
            Returns:
                int: 1 if available, 0 if unavailable, 8 if error
            """
            username = username.strip()
            
            try:
                result = check_api_function(username)
                
                if success_condition(result):
                    print(Fore.GREEN + success_message.format(username=username))
                    with available_lock:
                        with open(available_file, 'a') as f:
                            f.write(f"{username}\n")
                    with progress_lock:
                        with open(progress_file, 'a') as f:
                            f.write("1\n")
                    return 1
                else:
                    with unavailable_lock:
                        with open(unavailable_file, 'a') as f:
                            f.write(f"{username}\n")
                    with progress_lock:
                        with open(progress_file, 'a') as f:
                            f.write("1\n")
                    return 0
            except Exception as e:
                if error_message:
                    print(Fore.RED + error_message.format(username=username, error=e))
                return 8
        
        return check_function 