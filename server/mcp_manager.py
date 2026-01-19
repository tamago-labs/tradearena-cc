"""
MCP Manager for TradeArena
Handles multiple MCP clients and tool collection
"""

import json
import os
import logging
from typing import Dict, List, Any, Optional
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
        self.active_clients: Dict[str, MCPClient] = {}
    
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
            # Create MCP client using the pattern from the example
            client = MCPClient(lambda: stdio_client(
                StdioServerParameters(
                    command=server_config["command"],
                    args=server_config["args"]
                )
            ))
            logger.info(f"Created MCP client for {mcp_name}")
            return client
        except Exception as e:
            logger.error(f"Failed to create MCP client for {mcp_name}: {e}")
            return None
    
    @contextmanager
    def get_mcp_tools(self, trading_chain: str):
        """Context manager to get all tools for a specific trading chain"""
        required_mcps = self.get_required_mcps_for_chain(trading_chain)
        clients = []
        
        try:
            # Create and start all required MCP clients
            for mcp_name in required_mcps:
                client = self.create_mcp_client(mcp_name)
                if client:
                    clients.append((mcp_name, client))
                    client.__enter__()  # Start the client
                    logger.info(f"Started MCP client: {mcp_name}")
                else:
                    logger.warning(f"Failed to start MCP client: {mcp_name}")
            
            # Collect all tools from all clients
            all_tools = []
            for mcp_name, client in clients:
                try:
                    tools = client.list_tools_sync()
                    all_tools.extend(tools)
                    logger.info(f"Collected {len(tools)} tools from {mcp_name}")
                except Exception as e:
                    logger.error(f"Failed to get tools from {mcp_name}: {e}")
            
            yield all_tools
            
        finally:
            # Clean up all clients
            for mcp_name, client in clients:
                try:
                    client.__exit__(None, None, None)
                    logger.info(f"Stopped MCP client: {mcp_name}")
                except Exception as e:
                    logger.error(f"Error stopping MCP client {mcp_name}: {e}")

# Global MCP manager instance
mcp_manager = MCPManager()
