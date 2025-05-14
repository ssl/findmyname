import json
from pathlib import Path

class ConfigLoader:
    """Utility class to load configuration from the central config.json file."""
    
    @staticmethod
    def get_config_path():
        """Find the path to the config.json file by going one directory back."""
        current_dir = Path(__file__).parent
        main_dir = current_dir.parent
        config_path = main_dir / "config.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_path}")
        
        return config_path
    
    @staticmethod
    def load_config(tool_name=None):
        """Load configuration for a specific tool or the entire config."""
        config_path = ConfigLoader.get_config_path()
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            if tool_name:
                if tool_name not in config.get('tools', {}):
                    return {}
                
                # Return tool config
                tool_config = config['tools'][tool_name].copy()
                return tool_config
            
            return config
        
        except Exception as e:
            raise