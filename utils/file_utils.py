import os
import re
import time
import threading
import datetime
from colorama import Fore
from pathlib import Path

class FileUtils:
    """Utility class for file operations shared across all checkers."""
    
    @staticmethod
    def get_all_lines_from_input(input_path, script_dir=None):
        """
        Read all lines from an input file or directory.
        
        Args:
            input_path (str): Path to input file or directory
            script_dir (str, optional): Directory where the script is located
            
        Returns:
            list: List of lines from the input file(s)
        """
        # Use absolute path for input file if it's not a directory
        if not os.path.isdir(input_path):
            if not os.path.isabs(input_path) and script_dir:
                # If input file is relative, make it relative to the script directory
                input_path = os.path.join(script_dir, input_path)
        
        # Load input usernames with filtering
        if os.path.isdir(input_path):
            all_lines = FileUtils._get_all_lines_from_directory(input_path)
        else:
            # Try different encodings
            all_lines = FileUtils._read_file_with_multiple_encodings(input_path)
            
        return all_lines
    
    @staticmethod
    def _get_all_lines_from_directory(directory_path):
        """Read all lines from all files in a directory recursively."""
        all_lines = []
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r') as f:
                        all_lines.extend(f.readlines())
                except Exception as e:
                    print(Fore.RED + f"Error reading {file_path}: {e}")
        return all_lines
    
    @staticmethod
    def _read_file_with_multiple_encodings(file_path):
        """Try to read a file with multiple encodings."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.readlines()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                continue
        
        print(Fore.RED + f"Could not read file {file_path} with any of the attempted encodings")
        return []
    
    @staticmethod
    def setup_data_directory(tool_name, script_dir):
        """
        Set up the data directory for a tool and return paths to output files.
        
        Args:
            tool_name (str): Name of the tool (e.g., 'instagram', 'steam')
            script_dir (str): Directory where the script is located
            
        Returns:
            tuple: (data_dir, available_file, unavailable_file, sorted_available_file)
        """
        data_dir = os.path.join(script_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        available_file = os.path.join(data_dir, f'{tool_name}_available.txt')
        unavailable_file = os.path.join(data_dir, f'{tool_name}_unavailable.txt')
        sorted_available_file = os.path.join(data_dir, f'{tool_name}_sorted_available.txt')
        
        # Create files if they don't exist
        for file_path in [available_file, unavailable_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    pass
        
        return data_dir, available_file, unavailable_file, sorted_available_file
    
    @staticmethod
    def load_existing_results(available_file, unavailable_file):
        """
        Load existing results from available and unavailable files.
        
        Args:
            available_file (str): Path to available file
            unavailable_file (str): Path to unavailable file
            
        Returns:
            tuple: (available_set, unavailable_set)
        """
        if os.path.exists(available_file):
            with open(available_file, 'r') as f:
                available_set = set(line.strip().lower() for line in f if line.strip())
        else:
            available_set = set()
            with open(available_file, 'w') as f:
                pass

        if os.path.exists(unavailable_file):
            with open(unavailable_file, 'r') as f:
                unavailable_set = set(line.strip().lower() for line in f if line.strip())
        else:
            unavailable_set = set()
            with open(unavailable_file, 'w') as f:
                pass
                
        return available_set, unavailable_set
    
    @staticmethod
    def sort_and_save_results(available_file, sorted_available_file, sort_key=None):
        """
        Sort available results and save to a sorted file.
        
        Args:
            available_file (str): Path to available file
            sorted_available_file (str): Path to sorted available file
            sort_key (callable, optional): Function to use as sort key
        """
        print(Fore.BLUE + "Sorting available results...")
        
        try:
            with open(available_file, 'r') as f:
                available_items = [line.strip() for line in f if line.strip()]
            
            # Default sort key: by length first, then alphabetically
            if sort_key is None:
                sort_key = lambda x: (len(x), x)
            
            # Sort using the provided key
            sorted_items = sorted(available_items, key=sort_key)
            
            with open(sorted_available_file, 'w') as f:
                for item in sorted_items:
                    f.write(f"{item}\n")
            
            print(Fore.GREEN + f"Sorted {len(sorted_items)} items saved to {sorted_available_file}")
        except Exception as e:
            print(Fore.RED + f"Error sorting available items: {e}")
    
    @staticmethod
    def create_progress_monitor(progress_file, total_items, start_time, available_file, unavailable_file):
        """
        Create and start a progress monitor thread.
        
        Args:
            progress_file (str): Path to progress file
            total_items (int): Total number of items to process
            start_time (float): Start time of processing
            available_file (str): Path to available file
            unavailable_file (str): Path to unavailable file
            
        Returns:
            threading.Thread: The progress monitor thread
        """
        def progress_monitor():
            while True:
                try:
                    with open(progress_file, 'r') as f:
                        checked_items = len(f.readlines())
                    elapsed_time = time.time() - start_time
                    progress_percent = (checked_items / total_items) * 100 if total_items > 0 else 0
                    speed = checked_items / elapsed_time if elapsed_time > 0 else 0
                    eta = (total_items - checked_items) / speed if speed > 0 else 0
                    eta_str = f"ETA: {int(eta // 60)}m {int(eta % 60)}s"
                    
                    with open(available_file, 'r') as f:
                        total_available = sum(1 for line in f if line.strip())
                    with open(unavailable_file, 'r') as f:
                        total_unavailable = sum(1 for line in f if line.strip())
                    
                    print(Fore.CYAN + f"Progress: {checked_items}/{total_items} ({progress_percent:.2f}%) | "
                          f"TA: {total_available} | TU: {total_unavailable} | Speed: {speed:.2f} items/sec | {eta_str}")
                    
                    if checked_items >= total_items:
                        break
                    time.sleep(5)
                except Exception as e:
                    print(Fore.RED + f"Error in progress monitor: {e}")
                    time.sleep(5)
        
        # Create and start the progress monitor thread
        progress_thread = threading.Thread(target=progress_monitor)
        progress_thread.daemon = True
        progress_thread.start()
        
        return progress_thread
    
    @staticmethod
    def create_progress_file():
        """
        Create a progress file with a timestamp.
        
        Returns:
            tuple: (progress_file_path, timestamp)
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        progress_file = f'progress_{timestamp}.txt'
        
        with open(progress_file, 'w') as f:
            f.write("")
            
        return progress_file, timestamp
    
    @staticmethod
    def filter_usernames(usernames, min_length=5, max_length=15, valid_pattern=None):
        """
        Filter usernames based on common criteria.
        
        Args:
            usernames (list): List of usernames to filter
            min_length (int): Minimum username length
            max_length (int): Maximum username length
            valid_pattern (re.Pattern, optional): Regex pattern for valid usernames
            
        Returns:
            list: Filtered list of usernames
        """
        if valid_pattern is None:
            # Default pattern: a-z, 0-9, .
            valid_pattern = re.compile(r'^[a-z0-9.]+$')
        
        # Remove duplicates and invalid entries
        seen = set()
        filtered_usernames = []
        for username in usernames:
            username = username.strip().lower()
            if username and username not in seen and valid_pattern.match(username):
                seen.add(username)
                filtered_usernames.append(username)
        
        # Apply additional filters
        filtered_usernames = [u for u in filtered_usernames if len(u) >= min_length and len(u) <= max_length]
        
        return filtered_usernames 