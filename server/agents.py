"""
Agent configuration management for TradeArena
"""

import json
import os
import uuid
from typing import Dict, List, Any
from pathlib import Path

# Path to agent configurations file
AGENTS_FILE = Path(__file__).parent.parent / "config" / "config_agents.json"

class AgentManager:
    """Manage agent configurations"""
    
    def __init__(self):
        self.ensure_config_dir()
        self.agents = self.load_agents()
    
    def ensure_config_dir(self):
        """Ensure config directory exists"""
        config_dir = AGENTS_FILE.parent
        config_dir.mkdir(exist_ok=True)
    
    def load_agents(self) -> List[Dict[str, Any]]:
        """Load agents from file"""
        if not AGENTS_FILE.exists():
            # Start with empty agents list - no auto-creation
            return []
        
        try:
            with open(AGENTS_FILE, 'r') as f:
                data = json.load(f)
                return data.get("agents", [])
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_agents(self, agents: List[Dict[str, Any]]):
        """Save agents to file"""
        with open(AGENTS_FILE, 'w') as f:
            json.dump({"agents": agents}, f, indent=2)
        self.agents = agents
    
    def get_agents(self) -> List[Dict[str, Any]]:
        """Get all agents"""
        return self.agents
    
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get specific agent by ID"""
        for agent in self.agents:
            if agent["id"] == agent_id:
                return agent
        return None
    
    def create_agent(self, name: str = None, ai_provider: str = None, trading_chain: str = None, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create new agent with UUID-based ID and descriptive name"""
        # Generate UUID-based ID
        new_id = f"agent_{uuid.uuid4().hex[:8]}"
        
        # Create descriptive name if not provided
        if name is None:
            provider_name = next((p["name"] for p in AI_PROVIDERS if p["id"] == ai_provider), ai_provider)
            chain_name = next((c["name"] for c in TRADING_CHAINS if c["id"] == trading_chain), trading_chain)
            name = f"{provider_name} - {chain_name}"
        
        new_agent = {
            "id": new_id,
            "name": name,
            "ai_provider": ai_provider,
            "trading_chain": trading_chain
        }
        
        # Add configuration if provided
        if config:
            new_agent["config"] = config
        
        self.agents.append(new_agent)
        self.save_agents(self.agents)
        return new_agent
    
    def update_agent(self, agent_id: str, name: str = None, ai_provider: str = None, trading_chain: str = None) -> bool:
        """Update existing agent"""
        for agent in self.agents:
            if agent["id"] == agent_id:
                if name is not None:
                    agent["name"] = name
                if ai_provider is not None:
                    agent["ai_provider"] = ai_provider
                if trading_chain is not None:
                    agent["trading_chain"] = trading_chain
                self.save_agents(self.agents)
                return True
        return False
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete agent"""
        for i, agent in enumerate(self.agents):
            if agent["id"] == agent_id:
                del self.agents[i]
                self.save_agents(self.agents)
                return True
        return False

# Global agent manager instance
agent_manager = AgentManager()

# AI providers available
AI_PROVIDERS = [
    {"id": "amazon_bedrock", "name": "Amazon Bedrock"},
    {"id": "anthropic", "name": "Anthropic"},
    {"id": "gemini", "name": "Gemini"},
    {"id": "openai_compatible", "name": "OpenAI Compatible"}
]

# Trading chains available
TRADING_CHAINS = [
    {"id": "cronos", "name": "Cronos"},
    {"id": "kaia", "name": "Kaia"},
    {"id": "sui", "name": "Sui"},
    {"id": "aptos", "name": "Aptos"}
]

# Provider configuration specifications
PROVIDER_CONFIGS = {
    "amazon_bedrock": {
        "fields": ["model_id", "region_name"],
        "defaults": {
            "model_id": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            "region_name": "us-east-1"
        },
        "credentials_type": "aws_env",
        "display_name": "Amazon Bedrock"
    },
    "anthropic": {
        "fields": ["api_key", "model_id"],
        "defaults": {
            "model_id": "claude-sonnet-4-5-20250929"
        },
        "credentials_type": "api_key",
        "display_name": "Anthropic"
    },
    "gemini": {
        "fields": ["api_key", "model_id"],
        "defaults": {
            "model_id": "gemini-2.5-flash"
        },
        "credentials_type": "api_key",
        "display_name": "Gemini"
    },
    "openai_compatible": {
        "fields": ["api_key", "base_url", "model_id"],
        "defaults": {
            "model_id": "gpt-4o",
            "base_url": ""
        },
        "credentials_type": "api_key",
        "display_name": "OpenAI Compatible",
        "placeholders": {
            "base_url": "Leave blank for OpenAI server"
        }
    }
}
