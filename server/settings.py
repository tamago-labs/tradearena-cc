"""
Settings manager for TradeArena Web Terminal
Handles configuration persistence for Walrus and other settings
"""

import json
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SettingsManager:
    """Manages application settings persistence"""
    
    def __init__(self, settings_file: str = None):
        """Initialize settings manager with file path"""
        if settings_file is None:
            settings_dir = os.path.join(os.getcwd(), "config")
            os.makedirs(settings_dir, exist_ok=True)
            settings_file = os.path.join(settings_dir, "tradearena_settings.json")
        
        self.settings_file = settings_file
        self._default_settings = {
            "walrus": {
                "enabled": False
            },
            "web_search": {
                "enabled": False
            }
        }
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    logger.info(f"Loaded settings from {self.settings_file}")
                    # Only keep the enabled flag for walrus and web_search, ignore other fields
                    return self._clean_settings(settings)
            else:
                logger.info(f"Settings file not found, using defaults: {self.settings_file}")
                return self._default_settings.copy()
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return self._default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            # Clean settings to only include enabled flag for walrus and web_search
            clean_settings = self._clean_settings(settings)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(clean_settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings saved to {self.settings_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def is_walrus_enabled(self) -> bool:
        """Check if Walrus storage is enabled"""
        settings = self.load_settings()
        return settings.get("walrus", {}).get("enabled", False)
    
    def is_web_search_enabled(self) -> bool:
        """Check if web search is enabled"""
        settings = self.load_settings()
        return settings.get("web_search", {}).get("enabled", False)
    
    def get_walrus_settings(self) -> Dict[str, Any]:
        """Get Walrus-specific settings"""
        settings = self.load_settings()
        return settings.get("walrus", self._default_settings["walrus"])
    
    def get_web_search_settings(self) -> Dict[str, Any]:
        """Get web search-specific settings"""
        settings = self.load_settings()
        return settings.get("web_search", self._default_settings["web_search"])
    
    def save_walrus_settings(self, walrus_config: Dict[str, Any]) -> bool:
        """Save Walrus-specific settings"""
        # Only save the enabled flag
        clean_walrus_config = {"enabled": walrus_config.get("enabled", False)}
        settings = self.load_settings()
        settings["walrus"] = clean_walrus_config
        return self.save_settings(settings)
    
    def save_web_search_settings(self, web_search_config: Dict[str, Any]) -> bool:
        """Save web search-specific settings"""
        # Only save the enabled flag
        clean_web_search_config = {"enabled": web_search_config.get("enabled", False)}
        settings = self.load_settings()
        settings["web_search"] = clean_web_search_config
        return self.save_settings(settings)
    
    def _clean_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Clean settings to only include enabled flag for walrus and web_search"""
        clean_settings = self._default_settings.copy()
        
        for key, value in settings.items():
            if key in ["walrus", "web_search"]:
                # Only keep the enabled flag for these settings
                if isinstance(value, dict):
                    clean_settings[key] = {"enabled": value.get("enabled", False)}
                else:
                    clean_settings[key] = self._default_settings[key]
            else:
                # For other settings, keep as-is
                clean_settings[key] = value
        
        return clean_settings

# Global settings manager instance
settings_manager = SettingsManager()
