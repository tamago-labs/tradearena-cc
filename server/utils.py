"""
Configuration utilities for TradeArena Web Terminal
Preserved from original CLI implementation for web interface compatibility
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Manages configuration files and settings"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Configuration file paths
        self.agent_config_path = self.config_dir / "agent_config.yaml"
        self.view_config_path = self.config_dir / "view_config.json"
        self.walrus_config_path = self.config_dir / "walrus_config.json"
        
    def load_agent_config(self) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        default_config = {
            "ai_providers": {
                "anthropic": {
                    "enabled": True,
                    "model": "claude-3-sonnet-20240229",
                    "temperature": 0.7,
                    "max_tokens": 4000
                },
                "openai": {
                    "enabled": False,
                    "model": "gpt-4-turbo-preview",
                    "temperature": 0.7,
                    "max_tokens": 4000
                },
                "gemini": {
                    "enabled": False,
                    "model": "gemini-pro",
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            },
            "trading_chains": {
                "cronos": {
                    "enabled": True,
                    "rpc_url": "https://evm-cronos.crypto.org",
                    "explorer_url": "https://cronoscan.com"
                },
                "kaia": {
                    "enabled": True,
                    "rpc_url": "https://public-en-baobab.klaytn.net",
                    "explorer_url": "https://baobab.klaytnscope.com"
                },
                "sui": {
                    "enabled": False,
                    "rpc_url": "https://fullnode.mainnet.sui.io",
                    "explorer_url": "https://suiexplorer.com"
                },
                "aptos": {
                    "enabled": False,
                    "rpc_url": "https://fullnode.mainnet.aptoslabs.com",
                    "explorer_url": "https://explorer.aptoslabs.com"
                }
            },
            "risk_settings": {
                "max_trade_size_usd": 1000.0,
                "max_daily_trades": 50,
                "max_position_size_percent": 10.0,
                "stop_loss_percent": 5.0,
                "take_profit_percent": 10.0
            },
            "notifications": {
                "enabled": False,
                "discord_webhook": None,
                "telegram_bot_token": None,
                "telegram_chat_id": None
            }
        }
        
        if self.agent_config_path.exists():
            try:
                with open(self.agent_config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**default_config, **config}
            except Exception as e:
                print(f"Error loading agent config: {e}")
                return default_config
        else:
            # Create default config file
            self.save_agent_config(default_config)
            return default_config
    
    def save_agent_config(self, config: Dict[str, Any]) -> bool:
        """Save agent configuration to YAML file"""
        try:
            with open(self.agent_config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving agent config: {e}")
            return False
    
    def load_view_config(self) -> Dict[str, Any]:
        """Load view configuration from JSON file"""
        default_config = {
            "default_view": "trading_dashboard",
            "views": {
                "trading_dashboard": {
                    "name": "Trading Dashboard",
                    "description": "Main trading interface with real-time charts",
                    "widgets": ["portfolio", "recent_trades", "market_overview"]
                },
                "performance_analytics": {
                    "name": "Performance Analytics",
                    "description": "Detailed performance metrics and analysis",
                    "widgets": ["performance_chart", "profit_loss", "trade_statistics"]
                },
                "quick_trade": {
                    "name": "Quick Trade",
                    "description": "Simplified interface for fast trading",
                    "widgets": ["trade_form", "price_ticker"]
                }
            },
            "layout": {
                "theme": "dark",
                "refresh_interval": 5,
                "auto_scroll": True
            }
        }
        
        if self.view_config_path.exists():
            try:
                with open(self.view_config_path, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                print(f"Error loading view config: {e}")
                return default_config
        else:
            self.save_view_config(default_config)
            return default_config
    
    def save_view_config(self, config: Dict[str, Any]) -> bool:
        """Save view configuration to JSON file"""
        try:
            with open(self.view_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving view config: {e}")
            return False
    
    def load_walrus_config(self) -> Dict[str, Any]:
        """Load Walrus storage configuration from JSON file"""
        default_config = {
            "enabled": True,
            "endpoint": "https://walrus.ai",
            "publisher": "publisher.walrus.ai",
            "dealmaker": "dealmaker.walrus.ai",
            "aggregate": True,
            "epochs": 5,
            "prover": "groth16"
        }
        
        if self.walrus_config_path.exists():
            try:
                with open(self.walrus_config_path, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                print(f"Error loading Walrus config: {e}")
                return default_config
        else:
            self.save_walrus_config(default_config)
            return default_config
    
    def save_walrus_config(self, config: Dict[str, Any]) -> bool:
        """Save Walrus configuration to JSON file"""
        try:
            with open(self.walrus_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving Walrus config: {e}")
            return False

def validate_api_key(provider: str, api_key: str) -> bool:
    """Validate API key format for different providers"""
    if not api_key:
        return False
    
    if provider == "anthropic":
        return api_key.startswith("sk-ant-")
    elif provider == "openai":
        return api_key.startswith("sk-")
    elif provider == "gemini":
        return len(api_key) >= 30  # Basic validation for Gemini keys
    else:
        return len(api_key) >= 10  # Basic length validation

def get_environment_variable(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default value"""
    return os.getenv(name, default)

def ensure_config_directory(config_dir: str = "config") -> Path:
    """Ensure configuration directory exists and return Path object"""
    config_path = Path(config_dir)
    config_path.mkdir(exist_ok=True)
    
    # Create subdirectories
    (config_path / "logs").mkdir(exist_ok=True)
    (config_path / "backups").mkdir(exist_ok=True)
    (config_path / "exports").mkdir(exist_ok=True)
    
    return config_path

# Global configuration manager instance
config_manager = ConfigManager()

# Convenience functions
def get_agent_config() -> Dict[str, Any]:
    """Get current agent configuration"""
    return config_manager.load_agent_config()

def get_view_config() -> Dict[str, Any]:
    """Get current view configuration"""
    return config_manager.load_view_config()

def get_walrus_config() -> Dict[str, Any]:
    """Get current Walrus configuration"""
    return config_manager.load_walrus_config()

def update_agent_config(config: Dict[str, Any]) -> bool:
    """Update agent configuration"""
    return config_manager.save_agent_config(config)

def update_view_config(config: Dict[str, Any]) -> bool:
    """Update view configuration"""
    return config_manager.save_view_config(config)

def update_walrus_config(config: Dict[str, Any]) -> bool:
    """Update Walrus configuration"""
    return config_manager.save_walrus_config(config)