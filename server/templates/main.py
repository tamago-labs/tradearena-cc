"""
Main menu templates for TradeArena Web Terminal
"""

from ..static import MENU_JS
from .base import base_template, TRADE_ARENA_ASCII

def main_page_template(agents: list = None) -> str:
    """Main menu page template"""
    # Determine agent status based on agent count
    agent_count = len(agents) if agents else 0
    agent_status = "online" if agent_count > 0 else "warning"
    
    # Generate status text message
    if agent_count == 0:
        status_text = "Setup Required"
    elif agent_count == 1:
        status_text = "1 Agent Ready"
    else:
        status_text = f"{agent_count} Agents Ready"
    
    content = f"""
        <div class="terminal-header">
            <div class="ascii-art">{TRADE_ARENA_ASCII}</div>
            <div class="title">Vibe Trading Arena for AI Agents</div>
            <div class="subtitle">Cronos · Kaia · Sui</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">Main Menu</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="interactive">
                        <span class="status-indicator online"></span>Interactive Mode
                    </div>
                    <div class="menu-item" data-action="views">
                        <span class="status-indicator online"></span>Manage Views
                    </div>
                    <div class="menu-item" data-action="manage-agents">
                        <span class="status-indicator {agent_status}"></span>Manage Agents [{status_text}]
                    </div>
                    <div class="menu-item" data-action="settings">
                        <span class="status-indicator online"></span>Settings
                    </div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    return base_template("TradeArena Terminal", content, additional_js=MENU_JS)
