"""
Templates package for TradeArena Web Terminal

This package contains organized template modules for different parts of the application:
- base: Base template and shared components
- main: Main menu templates
- agents: Agent management templates
- interactive: Interactive mode and chat session templates
- views: Views management templates
- walrus: Walrus settings templates
"""

# Import all template functions for backward compatibility
from .base import base_template, TRADE_ARENA_ASCII
from .main import main_page_template
from .agents import (
    manage_agents_template,
    manage_agent_template,
    create_agent_template,
    create_agent_config_template,
    create_agent_step2_template,
    create_agent_confirm_template
)
from .interactive import (
    interactive_mode_template,
    select_agent_for_session_template,
    chat_session_template
)
from .views import views_page_template
from .walrus import walrus_settings_template

__all__ = [
    # Base templates
    'base_template',
    'TRADE_ARENA_ASCII',
    
    # Main templates
    'main_page_template',
    
    # Agent templates
    'manage_agents_template',
    'manage_agent_template',
    'create_agent_template',
    'create_agent_config_template',
    'create_agent_step2_template',
    'create_agent_confirm_template',
    
    # Interactive templates
    'interactive_mode_template',
    'select_agent_for_session_template',
    'chat_session_template',
    
    # Views templates
    'views_page_template',
    
    # Walrus templates
    'walrus_settings_template',
]
