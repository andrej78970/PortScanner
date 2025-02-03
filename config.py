import json

CONFIG_FILE = "config.json"

def load_config():
    """Loads the config file"""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "default_target": "127.0.0.1",
            "default_ports": "1-1000",
            "timeout": 0.5
        }

config = load_config()