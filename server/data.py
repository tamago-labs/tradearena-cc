"""
Mock data generators for TradeArena CLI web interface
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class MockDataGenerator:
    """Generate mock data for the web interface"""
    
    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        """Get default configuration settings"""
        return {
            "ai_providers": {
                "anthropic": {
                    "enabled": True,
                    "model": "claude-3-sonnet-20240229",
                    "api_key": "sk-ant-***masked***",
                    "temperature": 0.7,
                    "max_tokens": 4000
                },
                "openai": {
                    "enabled": False,
                    "model": "gpt-4-turbo-preview",
                    "api_key": "sk-***masked***",
                    "temperature": 0.7,
                    "max_tokens": 4000
                },
                "gemini": {
                    "enabled": False,
                    "model": "gemini-pro",
                    "api_key": "***masked***",
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            },
            "trading_chains": {
                "cronos": {
                    "enabled": True,
                    "rpc_url": "https://evm-cronos.crypto.org",
                    "explorer_url": "https://cronoscan.com",
                    "native_token": "CRO"
                },
                "kaia": {
                    "enabled": True,
                    "rpc_url": "https://public-en-baobab.klaytn.net",
                    "explorer_url": "https://baobab.klaytnscope.com",
                    "native_token": "KLAY"
                },
                "sui": {
                    "enabled": False,
                    "rpc_url": "https://fullnode.mainnet.sui.io",
                    "explorer_url": "https://suiexplorer.com",
                    "native_token": "SUI"
                },
                "aptos": {
                    "enabled": False,
                    "rpc_url": "https://fullnode.mainnet.aptoslabs.com",
                    "explorer_url": "https://explorer.aptoslabs.com",
                    "native_token": "APT"
                }
            },
            "storage": {
                "walrus": {
                    "enabled": True,
                    "endpoint": "https://walrus-testnet.walrus.ai",
                    "publisher_url": "https://publisher.walrus.ai",
                    "aggregator_url": "https://aggregator.walrus.ai"
                }
            },
            "risk_settings": {
                "max_trade_size_usd": 1000,
                "max_daily_trades": 50,
                "max_position_size_percent": 10,
                "stop_loss_percent": 5,
                "take_profit_percent": 15
            }
        }
    
    @staticmethod
    def get_agents() -> List[Dict[str, Any]]:
        """Get list of mock trading agents"""
        return [
            {
                "id": "agent_001",
                "name": "DeFi Yield Hunter",
                "status": "running",
                "type": "yield_farming",
                "chains": ["cronos", "kaia"],
                "created_at": "2024-01-15T10:30:00Z",
                "last_trade": "2024-01-20T14:25:00Z",
                "total_trades": 47,
                "success_rate": 78.5,
                "total_pnl": 1247.50,
                "current_position": {
                    "protocol": "VVS Finance",
                    "pair": "CRO/USDT",
                    "value": 850.00
                }
            },
            {
                "id": "agent_002", 
                "name": "Arbitrage Master",
                "status": "stopped",
                "type": "arbitrage",
                "chains": ["sui", "aptos"],
                "created_at": "2024-01-10T09:15:00Z",
                "last_trade": "2024-01-19T16:45:00Z",
                "total_trades": 23,
                "success_rate": 91.3,
                "total_pnl": 567.25,
                "current_position": None
            },
            {
                "id": "agent_003",
                "name": "Market Maker Bot",
                "status": "paused",
                "type": "market_making",
                "chains": ["cronos"],
                "created_at": "2024-01-08T11:20:00Z",
                "last_trade": "2024-01-20T12:30:00Z",
                "total_trades": 156,
                "success_rate": 65.8,
                "total_pnl": -234.75,
                "current_position": {
                    "protocol": "Moonlander",
                    "pair": "ETH/USDC",
                    "value": 1200.00
                }
            }
        ]
    
    @staticmethod
    def get_system_status() -> Dict[str, Any]:
        """Get system status information"""
        return {
            "server_status": "online",
            "uptime": "2d 14h 32m",
            "cpu_usage": 23.5,
            "memory_usage": 45.2,
            "disk_usage": 67.8,
            "active_agents": 1,
            "total_agents": 3,
            "last_backup": "2024-01-20T06:00:00Z",
            "version": "1.0.0",
            "chains_connected": ["cronos", "kaia"],
            "wallets_connected": 2
        }
    
    @staticmethod
    def get_recent_trades(limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent trading activity"""
        trades = []
        protocols = {
            "cronos": ["VVS Finance", "Moonlander", "Delphi"],
            "kaia": ["KiloLend", "DragonSwap"],
            "sui": ["Scallop", "Cetus"],
            "aptos": ["Thala", "Joule", "LiquidSwap"]
        }
        
        for i in range(limit):
            chain = random.choice(list(protocols.keys()))
            protocol = random.choice(protocols[chain])
            
            trade = {
                "id": f"trade_{i+1:03d}",
                "agent_id": random.choice(["agent_001", "agent_002", "agent_003"]),
                "timestamp": (datetime.now() - timedelta(minutes=i*15)).isoformat(),
                "chain": chain,
                "protocol": protocol,
                "action": random.choice(["buy", "sell", "deposit", "withdraw"]),
                "token_pair": random.choice([
                    "CRO/USDT", "ETH/USDC", "KLAY/USDT", 
                    "SUI/USDC", "APT/USDT", "WBTC/ETH"
                ]),
                "amount": round(random.uniform(100, 5000), 2),
                "price": round(random.uniform(0.1, 100), 4),
                "gas_used": round(random.uniform(0.001, 0.05), 6),
                "status": random.choice(["success", "pending", "failed"]),
                "pnl": round(random.uniform(-100, 200), 2) if random.random() > 0.3 else 0
            }
            trades.append(trade)
        
        return trades
    
    @staticmethod
    def get_performance_metrics() -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            "daily_pnl": {
                "today": 156.75,
                "yesterday": 89.25,
                "change_percent": 75.6
            },
            "weekly_pnl": {
                "current_week": 892.50,
                "last_week": 445.00,
                "change_percent": 100.6
            },
            "monthly_pnl": {
                "current_month": 3420.75,
                "last_month": 2780.00,
                "change_percent": 23.1
            },
            "trade_stats": {
                "total_trades": 226,
                "successful_trades": 178,
                "success_rate": 78.8,
                "avg_trade_size": 847.32,
                "avg_gas_cost": 0.0234
            },
            "agent_performance": [
                {
                    "agent_id": "agent_001",
                    "name": "DeFi Yield Hunter",
                    "pnl": 1247.50,
                    "trades": 47,
                    "success_rate": 78.5
                },
                {
                    "agent_id": "agent_002",
                    "name": "Arbitrage Master", 
                    "pnl": 567.25,
                    "trades": 23,
                    "success_rate": 91.3
                },
                {
                    "agent_id": "agent_003",
                    "name": "Market Maker Bot",
                    "pnl": -234.75,
                    "trades": 156,
                    "success_rate": 65.8
                }
            ]
        }