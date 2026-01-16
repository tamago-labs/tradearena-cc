"""
Session management utilities for TradeArena
Handles session listing, loading, and restoration
"""

import os
import json
import glob
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class SessionManager:
    """Manages session operations for the TradeArena chat system"""
    
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
                    
                    # Format session info
                    session_info = {
                        "session_id": session_data.get("session_id"),
                        "session_type": session_data.get("session_type", "UNKNOWN"),
                        "created_at": session_data.get("created_at"),
                        "updated_at": session_data.get("updated_at"),
                        "agent_info": agent_info,
                        "message_count": agent_info.get("message_count", 0),
                        "last_activity": self._get_last_activity(session_dir)
                    }
                    
                    sessions.append(session_info)
                except Exception as e:
                    print(f"[DEBUG] Error loading session {session_dir}: {e}")
                    continue
        
        # Sort by last activity (most recent first)
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return sessions
    
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
                print(f"[DEBUG] Error reading agent file: {e}")
        
        # Count messages
        message_files = glob.glob(os.path.join(agent_dir, "messages", "message_*.json"))
        agent_info["message_count"] = len(message_files)
        
        return agent_info
    
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
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
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
                    text_content = content[0].get("text", "")
                
                formatted_message = {
                    "role": message.get("role", "unknown"),
                    "content": text_content,
                    "message_id": message_data.get("message_id"),
                    "created_at": message_data.get("created_at"),
                    "updated_at": message_data.get("updated_at")
                }
                
                messages.append(formatted_message)
            except Exception as e:
                print(f"[DEBUG] Error loading message {message_file}: {e}")
                continue
        
        return messages
    
    def get_latest_session(self) -> Optional[Dict]:
        """Get the most recent session"""
        sessions = self.list_sessions()
        return sessions[0] if sessions else None
    
    def find_session_by_agent(self, agent_id: str) -> Optional[Dict]:
        """Find the most recent session for a specific agent"""
        sessions = self.list_sessions()
        
        for session in sessions:
            if session["agent_info"]["agent_id"] == agent_id:
                return session
        
        return None

# Global session manager instance
session_manager = SessionManager()
