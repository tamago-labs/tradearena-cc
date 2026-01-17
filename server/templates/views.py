"""
Views management templates for TradeArena Web Terminal
"""

from ..static import SUBMENU_JS
from .base import base_template

def views_page_template() -> str:
    """Views management page template"""
    content = """
        <div class="terminal-header">
            <div class="title">MANAGE VIEWS</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">View Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="no-views">No Views Available</div>
                    <div class="menu-item" data-action="back">Back to Main Menu</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = f"""
{SUBMENU_JS}

class ViewsMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'no-views':
                // Do nothing - just a placeholder
                break;
            case 'back':
                window.location.href = '/';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new ViewsMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Manage Views", content, additional_js=additional_js)
