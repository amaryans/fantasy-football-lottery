"""
Configuration manager for loading and managing application settings from JSON.
"""

import json
import os


class ConfigManager:
    """Manages application configuration from JSON file."""

    _instance = None
    _config = None

    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the configuration manager."""
        if self._config is None:
            self.config_path = "./config/league_config.json"
            self.load_config()

    def load_config(self):
        """Load configuration from JSON file, create default if not exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self._create_default_config()
        else:
            self._create_default_config()

    def _create_default_config(self):
        """Create a default configuration file."""
        self._config = {
            "league_name": "West KTown Fantasy Football League",
            "number_of_teams": 12,
            "logo_path": "./data/wktownffbllogo.png",
            "owners": [
                {
                    "owner": "Owen",
                    "team_name": "Owen-Wan Kenobi",
                    "record": "9-5",
                    "image_path": "./data/owen.jpeg"
                },
                {
                    "owner": "Batches",
                    "team_name": "Darth Batches",
                    "record": "7-7",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Jakeb",
                    "team_name": "Sunny In Philadelphia",
                    "record": "10-4",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Addi",
                    "team_name": "Anazyn Skywalkers",
                    "record": "9-5",
                    "image_path": "./data/addi.JPEG"
                },
                {
                    "owner": "Austin",
                    "team_name": "Sacraficial Lambs",
                    "record": "8-6",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Sam",
                    "team_name": "Batman and Robinson",
                    "record": "7-7",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Beans",
                    "team_name": "Fuck Stefon Diggs",
                    "record": "6-8",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Logan",
                    "team_name": "Clark Street Dawgs",
                    "record": "6-8",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Gus",
                    "team_name": "Bitch Cup",
                    "record": "5-9",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Carson",
                    "team_name": "Euro Trash'd",
                    "record": "6-8",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "Dom",
                    "team_name": "domthebomb44",
                    "record": "4-10",
                    "image_path": "./data/wktownffbllogo.png"
                },
                {
                    "owner": "TCoop",
                    "team_name": "Magic Mike Tython",
                    "record": "7-7",
                    "image_path": "./data/wktownffbllogo.png"
                }
            ]
        }
        self.save_config()

    def save_config(self):
        """Save current configuration to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def reload_config(self):
        """Reload configuration from file."""
        self.load_config()

    @property
    def league_name(self):
        """Get league name."""
        return self._config.get("league_name", "Fantasy Football League")

    @property
    def number_of_teams(self):
        """Get number of teams."""
        return self._config.get("number_of_teams", 12)

    @property
    def logo_path(self):
        """Get league logo path."""
        return self._config.get("logo_path", "./data/wktownffbllogo.png")

    @property
    def owners(self):
        """Get list of owner dictionaries."""
        return self._config.get("owners", [])

    @property
    def owner_images(self):
        """Get dictionary mapping owner names to image paths."""
        return {owner["owner"]: owner["image_path"] for owner in self.owners}

    @property
    def owner_names(self):
        """Get list of owner names."""
        return [owner["owner"] for owner in self.owners]

    def get_standings_data(self):
        """
        Get standings data in the format expected by the standings widget.

        Returns:
            List of lists containing [owner, team_name, record]
        """
        return [[owner["owner"], owner["team_name"], owner["record"]] for owner in self.owners]

    def get_owner_by_name(self, name):
        """
        Get owner data by owner name.

        Args:
            name: Owner name to search for

        Returns:
            Owner dictionary or None if not found
        """
        for owner in self.owners:
            if owner["owner"] == name:
                return owner
        return None


# Global config instance
config = ConfigManager()
