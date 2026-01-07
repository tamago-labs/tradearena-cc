"""
CLI Utilities for TradeArena
"""
import json
import os
from typing import Dict, Any
from pathlib import Path


class ConfigManager:
    """Manages CLI configuration"""
    
    def __init__(self):
        self.config_file = Path("config/settings.json")
        self.config_file.parent.mkdir(exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "agent": {
                "model": {
                    "provider": "OpenAI",
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 4000
                },
                "mcp_tools": {
                    "sui": {
                        "navi_protocol": False,
                        "scallop": False,
                        "validator_staking": False
                    },
                    "kaia": {
                        "kilolend": False,
                        "dragonswap": False
                    },
                    "cronos": {
                        "moonlander": False,
                        "delphi": False,
                        "vvs_finance": False,
                        "cronos_x402": False
                    }
                },
                "strategy": {
                    "template": "balanced",
                    "max_position_size": 1000,
                    "drawdown_limit": 0.1
                }
            },
            "html_interface": {
                "enabled": True,
                "port": 5173
            },
            "walrus": {
                "enabled": False,
                "visibility": "private"
            },
            "sessions": {}
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()


class MockServices:
    """Mock services for demonstration"""
    
    @staticmethod
    def start_agent_session(session_type: str = "new") -> str:
        """Mock agent session start"""
        if session_type == "new":
            return "Started new interactive agent session"
        else:
            return "Resumed last agent session"
    
    @staticmethod
    def start_scheduled_agent(schedule_config: dict) -> str:
        """Mock scheduled agent start"""
        return f"Started scheduled agent with config: {schedule_config}"
    
    @staticmethod
    def get_running_agents() -> list:
        """Mock running agents list"""
        return [
            {"id": "agent_001", "name": "Vibe Trader", "status": "running", "schedule": "every 5 minutes"},
            {"id": "agent_002", "name": "DeFi Arbitrage", "status": "paused", "schedule": "hourly"}
        ]
    
    @staticmethod
    def get_agent_logs() -> list:
        """Mock agent logs"""
        return [
            {"timestamp": "2024-01-07 12:00:00", "action": "BUY", "token": "ETH", "amount": 100, "price": 2500},
            {"timestamp": "2024-01-07 12:05:00", "action": "SELL", "token": "BTC", "amount": 0.5, "price": 45000},
            {"timestamp": "2024-01-07 12:10:00", "action": "STAKE", "token": "SUI", "amount": 500, "validator": "validator_123"}
        ]
    
    @staticmethod
    def get_walrus_records() -> list:
        """Mock Walrus storage records"""
        return [
            {"id": "record_001", "type": "trade_decision", "timestamp": "2024-01-07 12:00:00", "size": "2.3KB"},
            {"id": "record_002", "type": "analysis", "timestamp": "2024-01-07 12:05:00", "size": "1.1KB"},
            {"id": "record_003", "type": "portfolio_state", "timestamp": "2024-01-07 12:10:00", "size": "3.7KB"}
        ]
    
    @staticmethod
    def get_available_views() -> list:
        """Mock available dashboard views"""
        return [
            {"name": "Portfolio Overview", "type": "dashboard", "last_updated": "2024-01-07 12:15:00"},
            {"name": "Trade History", "type": "chart", "last_updated": "2024-01-07 12:10:00"},
            {"name": "Strategy Performance", "type": "analytics", "last_updated": "2024-01-07 12:05:00"}
        ]