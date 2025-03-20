import json
import os

class GameConfig:
    def __init__(self):
        self.config_file = "config/settings.json"
        self.default_config = {
            "window": {
                "width": 640,
                "height": 480,
                "title": "Super Mario Python",
                "fps": 60
            },
            "game": {
                "gravity": 0.8,
                "jump_force": -15,
                "move_speed": 2,
                "max_lives": 3,
                "invincibility_duration": 60,
                "coin_value": 100
            },
            "audio": {
                "volume": 0.5,
                "music_enabled": True,
                "sfx_enabled": True
            },
            "controls": {
                "left": "K_LEFT",
                "right": "K_RIGHT",
                "jump": "K_SPACE",
                "pause": "K_p"
            }
        }
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.default_config
        return self.default_config

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        """Get a config value using dot notation (e.g., 'window.width')"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key, value):
        """Set a config value using dot notation (e.g., 'window.width')"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save_config()

    def reset_to_default(self):
        """Reset all settings to default values"""
        self.config = self.default_config.copy()
        self.save_config() 