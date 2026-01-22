"""
MCP Manager for TradeArena
Handles multiple MCP clients and tool collection
"""

import json
import os
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from contextlib import contextmanager
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

logger = logging.getLogger(__name__)

class MCPManager:
    """Manages multiple MCP clients for different chains"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.getcwd(), "config", "mcp_config.json")
        
        self.config_path = config_path
        self.config = self._load_config()
        self.active_clients: Dict[str, Tuple[MCPClient, Any]] = {}  # (client, session)
        self._load_credentials()
    
    def _load_credentials(self) -> None:
        """Load environment variables from CREDENTIALS_ENV or credentials.env file"""
        
        # Check if credentials content is provided in environment variable
        credentials_env = os.getenv("CREDENTIALS_ENV")
        
        if credentials_env:
            # Parse key-value pairs from CREDENTIALS_ENV content
            logger.info("Loading credentials from CREDENTIALS_ENV environment variable")
            for line in credentials_env.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
            logger.info("Credentials loaded successfully from environment variable")
        else:
            # Default to loading from config/credentials.env file
            credentials_path = os.path.join(os.getcwd(), "config", "credentials.env")
            logger.info(f"CREDENTIALS_ENV not set, loading from file: {credentials_path}")
            
            try:
                if os.path.exists(credentials_path):
                    with open(credentials_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                os.environ[key.strip()] = value.strip()
                    logger.info("Credentials loaded successfully from file")
                else:
                    logger.warning(f"Credentials file not found at {credentials_path}")
            except Exception as e:
                logger.error(f"Failed to load credentials from file: {e}")
    
    def _substitute_env_vars(self, text: str) -> str:
        """Substitute environment variables in text using ${VAR} pattern"""
        if not isinstance(text, str):
            return text
        
        def replace_var(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))
        
        # Pattern to match ${VARIABLE_NAME}
        pattern = r'\$\{([^}]+)\}'
        return re.sub(pattern, replace_var, text)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load MCP config from {self.config_path}: {e}")
            return {"mcp_servers": {}, "chain_mappings": {}}
    
    def get_required_mcps_for_chain(self, trading_chain: str) -> List[str]:
        """Get list of required MCP servers for a specific trading chain"""
        chain_mappings = self.config.get("chain_mappings", {})
        return chain_mappings.get(trading_chain, ["core-mcp"])
    
    def create_mcp_client(self, mcp_name: str) -> Optional[MCPClient]:
        """Create an MCP client for the specified server"""
        mcp_servers = self.config.get("mcp_servers", {})
        server_config = mcp_servers.get(mcp_name)
        
        if not server_config:
            logger.error(f"MCP server config not found: {mcp_name}")
            return None
        
        try:
            # Process environment variables and substitutions
            env_vars = {}
            if "env" in server_config:
                for key, value in server_config["env"].items():
                    env_vars[key] = self._substitute_env_vars(value)
            
            # Substitute environment variables in args
            processed_args = []
            for arg in server_config["args"]:
                processed_args.append(self._substitute_env_vars(arg))
            
            # Create MCP client with environment variables
            client = MCPClient(lambda: stdio_client(
                StdioServerParameters(
                    command=server_config["command"],
                    args=processed_args,
                    env=env_vars if env_vars else None
                )
            ))
            logger.info(f"Created MCP client for {mcp_name}")
            return client
        except Exception as e:
            logger.error(f"Failed to create MCP client for {mcp_name}: {e}")
            return None
    
    def initialize_mcp_clients(self, trading_chain: str) -> Dict[str, Tuple[MCPClient, Any]]:
        """Initialize and maintain persistent MCP clients for a trading chain"""
        required_mcps = self.get_required_mcps_for_chain(trading_chain)
        persistent_clients = {}
        
        for mcp_name in required_mcps:
            if mcp_name in self.active_clients:
                # Reuse existing client
                persistent_clients[mcp_name] = self.active_clients[mcp_name]
                logger.info(f"Reusing existing MCP client for {mcp_name}")
            else:
                # Create new persistent client
                client = self.create_mcp_client(mcp_name)
                if not client:
                    logger.warning(f"Failed to create MCP client: {mcp_name}")
                    continue
                
                try:
                    # Start the client and keep the session alive
                    session = client.__enter__()
                    persistent_clients[mcp_name] = (client, session)
                    self.active_clients[mcp_name] = (client, session)
                    logger.info(f"Initialized persistent MCP client for {mcp_name}")
                except Exception as e:
                    logger.error(f"Failed to initialize MCP client {mcp_name}: {e}")
        
        return persistent_clients
    
    def get_mcp_tools(self, trading_chain: str) -> Tuple[List[Any], Dict[str, Tuple[MCPClient, Any]]]:
        """Get all tools for a specific trading chain and return persistent clients"""
        # Initialize persistent clients
        persistent_clients = self.initialize_mcp_clients(trading_chain)
        all_tools = []
        
        for mcp_name, (client, session) in persistent_clients.items():
            try:
                # Extract tools from the persistent session
                tools = client.list_tools_sync()
                all_tools.extend(tools)
                logger.info(f"Successfully collected {len(tools)} tools from {mcp_name}")
            except Exception as e:
                logger.error(f"Failed to get tools from {mcp_name}: {e}")
        
        return all_tools, persistent_clients
    
    def close_clients(self, trading_chain: str = None):
        """Close MCP clients for a specific chain or all clients"""
        if trading_chain:
            # Close specific chain clients
            required_mcps = self.get_required_mcps_for_chain(trading_chain)
            for mcp_name in required_mcps:
                if mcp_name in self.active_clients:
                    client, session = self.active_clients[mcp_name]
                    try:
                        client.__exit__(None, None, None)
                        logger.info(f"Closed MCP client for {mcp_name}")
                    except Exception as e:
                        logger.error(f"Error closing MCP client {mcp_name}: {e}")
                    finally:
                        del self.active_clients[mcp_name]
        else:
            # Close all clients
            for mcp_name, (client, session) in self.active_clients.items():
                try:
                    client.__exit__(None, None, None)
                    logger.info(f"Closed MCP client for {mcp_name}")
                except Exception as e:
                    logger.error(f"Error closing MCP client {mcp_name}: {e}")
            self.active_clients.clear()

# Global MCP manager instance
mcp_manager = MCPManager()
