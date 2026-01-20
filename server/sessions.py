"""
Session management for TradeArena
Handles agent session persistence and retrieval
"""

import os
import json
import glob
import logging
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SessionManager:
    """Manages agent sessions with persistent storage"""
    
    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = sessions_dir
        os.makedirs(sessions_dir, exist_ok=True)
    
    def list_sessions(self) -> List[Dict]:
        """List all available sessions with metadata"""
        sessions = []
        
        # Find all session directories
        session_dirs = glob.glob(os.path.join(self.sessions_dir, "session_*"))
        
        for session_dir in session_dirs:
            session_file = os.path.join(session_dir, "session.json")
            if os.path.exists(session_file):
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    # Extract agent information
                    agent_info = self._extract_agent_info(session_dir)
                    
                    # Calculate session size
                    session_size = self._calculate_session_size(session_dir)
                    
                    # Format session info
                    session_info = {
                        "session_id": session_data.get("session_id"),
                        "session_type": session_data.get("session_type", "UNKNOWN"),
                        "created_at": session_data.get("created_at"),
                        "updated_at": session_data.get("updated_at"),
                        "agent_info": agent_info,
                        "message_count": agent_info.get("message_count", 0),
                        "file_size": session_size,
                        "last_activity": self._get_last_activity(session_dir)
                    }
                    
                    sessions.append(session_info)
                except Exception as e:
                    logger.error(f"Error loading session {session_dir}: {e}")
                    continue
        
        # Sort by last activity (most recent first)
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return sessions
    
    def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Load all messages from a specific session"""
        session_dir = os.path.join(self.sessions_dir, f"session_{session_id}")
        
        if not os.path.exists(session_dir):
            return []
        
        # Find agent directory
        agent_dirs = glob.glob(os.path.join(session_dir, "agents", "agent_*"))
        if not agent_dirs:
            return []
        
        agent_dir = agent_dirs[0]
        message_files = glob.glob(os.path.join(agent_dir, "messages", "message_*.json"))
        
        # Sort messages by ID
        message_files.sort(key=lambda x: int(os.path.basename(x).split("_")[1].split(".")[0]))
        
        messages = []
        for message_file in message_files:
            try:
                with open(message_file, 'r') as f:
                    message_data = json.load(f)
                    
                # Extract text content
                message = message_data.get("message", {})
                content = message.get("content", [])
                
                text_content = ""
                if content and len(content) > 0:
                    # Handle new message structure with reasoningContent and text
                    for content_item in content:
                        if isinstance(content_item, dict):
                            # Look for direct text content (not reasoningContent)
                            if "text" in content_item and content_item["text"].strip():
                                text_content = content_item["text"]
                                logger.debug(f"Found text content: {text_content[:100]}...")
                                break
                            # Handle old structure as fallback
                            elif "text" in content_item:
                                text_content = content_item["text"]
                
                formatted_message = {
                    "role": message.get("role", "unknown"),
                    "content": text_content,
                    "message_id": message_data.get("message_id"),
                    "created_at": message_data.get("created_at"),
                    "updated_at": message_data.get("updated_at")
                }
                
                # Only add messages with actual content (filter out blank/empty messages)
                if text_content and text_content.strip():
                    messages.append(formatted_message)
                else:
                    logger.debug(f"Skipping blank message: {message_data.get('message_id')}")
            except Exception as e:
                logger.error(f"Error loading message {message_file}: {e}")
                continue
        
        return messages
    
    def get_latest_session(self) -> Optional[Dict[str, Any]]:
        """Get the most recent session"""
        sessions = self.list_sessions()
        return sessions[0] if sessions else None
    
    def _extract_agent_info(self, session_dir: str) -> Dict:
        """Extract agent information from session directory"""
        agent_dirs = glob.glob(os.path.join(session_dir, "agents", "agent_*"))
        
        if not agent_dirs:
            return {"agent_id": None, "message_count": 0}
        
        agent_dir = agent_dirs[0]  # Take first agent
        
        # Get agent info from agent.json
        agent_file = os.path.join(agent_dir, "agent.json")
        agent_info = {"agent_id": None, "message_count": 0}
        
        if os.path.exists(agent_file):
            try:
                with open(agent_file, 'r') as f:
                    agent_data = json.load(f)
                    agent_info["agent_id"] = agent_data.get("agent_id")
            except Exception as e:
                logger.error(f"Error reading agent file: {e}")
        
        # Count messages
        message_files = glob.glob(os.path.join(agent_dir, "messages", "message_*.json"))
        agent_info["message_count"] = len(message_files)
        
        # Enhance with agent configuration details
        agent_info = self._enhance_agent_info(agent_info)
        
        return agent_info
    
    def _enhance_agent_info(self, agent_info: Dict) -> Dict:
        """Enhance agent info with configuration details from agent state or agent manager"""
        try:
            # Import here to avoid circular imports
            try:
                from .agents import AI_PROVIDERS
            except ImportError:
                # Fallback for direct execution
                from agents import AI_PROVIDERS
            
            agent_id = agent_info.get("agent_id")
            if not agent_id:
                return agent_info
            
            # First try to get agent config from agent state (preferred method)
            agent_config_from_state = self._get_agent_config_from_state(agent_id)
            
            if agent_config_from_state:
                agent_info["ai_provider"] = agent_config_from_state.get("ai_provider", "unknown")
                agent_info["trading_chain"] = agent_config_from_state.get("trading_chain", "unknown")
                agent_info["name"] = agent_config_from_state.get("name", "Unknown Agent")
                agent_info["config_agent_id"] = agent_config_from_state.get("id")  # Short ID for config retrieval
                
                # Get provider display name
                provider_id = agent_config_from_state.get("ai_provider", "")
                provider_display = self._get_provider_display_name(provider_id)
                agent_info["ai_provider_display"] = provider_display
            else:
                # Fallback to agent manager (for backward compatibility)
                agent_config_from_manager = self._get_agent_config_from_manager(agent_id)
                if agent_config_from_manager:
                    agent_info["ai_provider"] = agent_config_from_manager.get("ai_provider", "unknown")
                    agent_info["trading_chain"] = agent_config_from_manager.get("trading_chain", "unknown")
                    
                    # Get provider display name
                    provider_id = agent_config_from_manager.get("ai_provider", "")
                    provider_display = self._get_provider_display_name(provider_id)
                    agent_info["ai_provider_display"] = provider_display
                else:
                    agent_info["ai_provider"] = "unknown"
                    agent_info["ai_provider_display"] = "Unknown"
                    agent_info["trading_chain"] = "unknown"
                
        except Exception as e:
            logger.error(f"Error enhancing agent info: {e}")
            agent_info["ai_provider"] = "unknown"
            agent_info["ai_provider_display"] = "Unknown"
            agent_info["trading_chain"] = "unknown"
        
        return agent_info
    
    def _get_agent_config_from_state(self, agent_id: str) -> Dict:
        """Extract agent configuration from agent's saved state"""
        try:
            # Find the agent directory for this session
            session_dirs = glob.glob(os.path.join(self.sessions_dir, "session_*"))
            
            for session_dir in session_dirs:
                # Look for agent directories that might contain this agent
                # Try multiple patterns to handle different directory naming conventions
                agent_patterns = [
                    f"agent_{agent_id}*",
                    f"agent_trading_agent_{agent_id}*",
                    f"trading_agent_{agent_id}*"
                ]
                
                for pattern in agent_patterns:
                    agent_dirs = glob.glob(os.path.join(session_dir, "agents", pattern))
                    
                    for agent_dir in agent_dirs:
                        # Check agent.json file
                        agent_file = os.path.join(agent_dir, "agent.json")
                        if os.path.exists(agent_file):
                            with open(agent_file, 'r') as f:
                                agent_data = json.load(f)
                            
                            # Extract config from agent state
                            state = agent_data.get("state", {})
                            agent_config = state.get("agent_config", {})
                            
                            if agent_config:
                                logger.debug(f"Found agent config in state: {agent_config}")
                                return agent_config
            
            logger.debug(f"No agent config found in state for agent_id: {agent_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting agent config from state: {e}")
            return None
    
    def _get_agent_config_from_manager(self, agent_id: str) -> Dict:
        """Fallback: Get agent configuration from agent manager"""
        try:
            # Import here to avoid circular imports
            try:
                from .agents import agent_manager
            except ImportError:
                # Fallback for direct execution
                from agents import agent_manager
            
            # Extract short agent ID (remove "trading_agent_agent_" prefix if present)
            if agent_id.startswith("trading_agent_agent_"):
                short_agent_id = "agent_" + agent_id.replace("trading_agent_agent_", "")
            else:
                short_agent_id = agent_id
            
            # Get agent configuration
            agent_config = agent_manager.get_agent(short_agent_id)
            return agent_config
            
        except Exception as e:
            logger.error(f"Error getting agent config from manager: {e}")
            return None
    
    def _get_provider_display_name(self, provider_id: str) -> str:
        """Get display name for AI provider"""
        # Import here to avoid circular imports
        try:
            from .agents import AI_PROVIDERS
        except ImportError:
            # Fallback if import fails
            AI_PROVIDERS = [
                {"id": "amazon_bedrock", "name": "Amazon Bedrock"},
                {"id": "anthropic", "name": "Anthropic"},
                {"id": "gemini", "name": "Gemini"},
                {"id": "openai_compatible", "name": "OpenAI Compatible"}
            ]
        
        # Handle provider ID mapping for consistency
        provider_mapping = {
            "amazon-bedrock": "amazon_bedrock",
            "openai-compatible": "openai_compatible",
            "openai compatible": "openai_compatible"
        }
        
        # Normalize provider ID
        normalized_provider_id = provider_mapping.get(provider_id, provider_id)
        
        provider_display = "Unknown"
        for provider in AI_PROVIDERS:
            if provider["id"] == normalized_provider_id:
                provider_display = provider["name"]
                break
        
        # If still unknown, try to create a display name from the provider_id
        if provider_display == "Unknown" and provider_id:
            provider_display = provider_id.replace("-", " ").replace("_", " ").title()
        
        return provider_display
    
    def _calculate_session_size(self, session_dir: str) -> str:
        """Calculate total size of session files in human-readable format"""
        total_size = 0
        
        # Calculate size of all JSON files in the session
        for root, dirs, files in os.walk(session_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except OSError:
                        continue
        
        # Convert to human-readable format
        if total_size < 1024:
            return f"{total_size}B"
        elif total_size < 1024 * 1024:
            return f"{total_size // 1024}KB"
        else:
            return f"{total_size // (1024 * 1024)}MB"
    
    def _get_last_activity(self, session_dir: str) -> str:
        """Get the last activity timestamp from the session"""
        try:
            # Check session.json first
            session_file = os.path.join(session_dir, "session.json")
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    return session_data.get("updated_at", "")
        except Exception:
            pass
        
        return ""
    
    def find_session_by_agent(self, agent_id: str) -> Optional[Dict]:
        """Find the most recent session for a specific agent"""
        sessions = self.list_sessions()
        
        for session in sessions:
            if session["agent_info"]["agent_id"] == agent_id:
                return session
        
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete an entire session directory and all its contents"""
        session_dir = os.path.join(self.sessions_dir, f"session_{session_id}")
        
        if not os.path.exists(session_dir):
            logger.warning(f"Session directory does not exist: {session_dir}")
            return False
        
        try:
            # Remove the entire session directory and all its contents
            shutil.rmtree(session_dir)
            logger.info(f"Successfully deleted session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False

    def get_agent_config_for_resume(self, session_id: str) -> Optional[Dict]:
        """Get agent configuration for resuming a session"""
        session_dir = os.path.join(self.sessions_dir, f"session_{session_id}")
        
        if not os.path.exists(session_dir):
            return None
        
        # Find agent directory
        agent_dirs = glob.glob(os.path.join(session_dir, "agents", "agent_*"))
        if not agent_dirs:
            return None
        
        agent_dir = agent_dirs[0]
        agent_file = os.path.join(agent_dir, "agent.json")
        
        if os.path.exists(agent_file):
            try:
                with open(agent_file, 'r') as f:
                    agent_data = json.load(f)
                
                # Extract config from agent state
                state = agent_data.get("state", {})
                agent_config = state.get("agent_config", {})
                
                if agent_config:
                    logger.debug(f"Found agent config for resume: {agent_config}")
                    return agent_config
                    
            except Exception as e:
                logger.error(f"Error getting agent config for resume: {e}")
        
        return None

# Global session manager instance
session_manager = SessionManager()
