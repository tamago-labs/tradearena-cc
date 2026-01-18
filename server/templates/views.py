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
                <div class="menu-header">Available Views</div>
                <div id="menuItems">
                    <div class="menu-item loading" data-action="loading">Loading views...</div>
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
    constructor() {{
        super();
        this.loadViews();
    }}
    
    async loadViews() {{
        try {{
            const response = await fetch('/api/views');
            const data = await response.json();
            const menuItems = document.getElementById('menuItems');
            
            // Clear existing items except the back button
            const backButton = menuItems.querySelector('[data-action="back"]');
            menuItems.innerHTML = '';
            
            if (data.views && data.views.length > 0) {{
                // Add views to menu
                data.views.forEach((view, index) => {{
                    const createdDate = new Date(view.created_at).toLocaleDateString();
                    const menuItem = document.createElement('div');
                    menuItem.className = 'menu-item';
                    menuItem.setAttribute('data-action', 'view-' + index);
                    menuItem.setAttribute('data-filename', view.filename);
                    const agentInfo = view.agent_name ? `Created by ${{view.agent_name}} • ${{createdDate}}` : `Created on ${{createdDate}}`;
                    menuItem.innerHTML = `
                        <div class="view-content">
                            <div class="view-title">${{view.title}}</div>
                            <div class="view-meta">${{agentInfo}}</div>
                        </div>
                        <div class="view-actions">
                            <button class="view-button open-btn" onclick="viewsMenu.openView('${{view.filename}}')">Open</button>
                            <button class="view-button delete-btn" onclick="viewsMenu.deleteView('${{view.filename}}', '${{view.title}}')">Delete</button>
                        </div>
                    `;
                    menuItems.appendChild(menuItem);
                }});
            }} else {{
                const noViewsItem = document.createElement('div');
                noViewsItem.className = 'menu-item';
                noViewsItem.setAttribute('data-action', 'no-views');
                noViewsItem.textContent = 'No Views Available';
                menuItems.appendChild(noViewsItem);
            }}
            
            // Add back button
            menuItems.appendChild(backButton);
            
            // Reinitialize menu items
            this.menuItems = menuItems.querySelectorAll('.menu-item');
            this.selectedIndex = 0;
            this.updateSelection();
            
        }} catch (error) {{
            console.error('Error loading views:', error);
            const menuItems = document.getElementById('menuItems');
            const errorItem = document.createElement('div');
            errorItem.className = 'menu-item';
            errorItem.setAttribute('data-action', 'error');
            errorItem.textContent = 'Error loading views';
            menuItems.insertBefore(errorItem, menuItems.firstChild);
        }}
    }}
    
    openView(filename) {{
        window.open(`/views/${{filename}}`, '_blank');
    }}
    
    async deleteView(filename, title) {{
        if (confirm(`Are you sure you want to delete "${{title}}"? This action cannot be undone.`)) {{
            try {{
                const response = await fetch(`/api/views/${{filename}}`, {{
                    method: 'DELETE'
                }});
                const result = await response.json();
                
                if (result.success) {{
                    alert('View deleted successfully');
                    this.loadViews(); // Refresh the list
                }} else {{
                    alert('Error deleting view: ' + (result.error || 'Unknown error'));
                }}
            }} catch (error) {{
                console.error('Error deleting view:', error);
                alert('Error deleting view: ' + error.message);
            }}
        }}
    }}
    
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        // Only handle non-view actions in select method
        // View actions are handled by button clicks
        if (!action.startsWith('view-')) {{
            switch(action) {{
                case 'no-views':
                    // Do nothing - just a placeholder
                    break;
                case 'back':
                    window.location.href = '/';
                    break;
                case 'error':
                    // Retry loading views
                    this.loadViews();
                    break;
            }}
        }}
    }}
}}

// Global instance for button access
let viewsMenu;

document.addEventListener('DOMContentLoaded', () => {{
    viewsMenu = new ViewsMenu();
}});
    """
    
    additional_css = """
    <style>
    .view-title {
        font-weight: bold;
        color: #00ff00;
    }
    
    .view-meta {
        font-size: 0.8em;
        color: #888;
        margin-top: 2px;
    }
    
    .loading {
        color: #ffff00;
    }
    
    .view-content {
        flex: 1;
    }
    
    .view-actions {
        display: flex;
        gap: 5px;
        margin-left: 10px;
    }
    
    .view-button {
        padding: 4px 8px;
        font-size: 0.75em;
        border: 1px solid #333;
        border-radius: 3px;
        cursor: pointer;
        font-family: 'Courier New', monospace;
        transition: all 0.2s;
    }
    
    .open-btn {
        background-color: #003300;
        color: #00ff00;
    }
    
    .open-btn:hover {
        background-color: #005500;
    }
    
    .delete-btn {
        background-color: #003300;
        color: #00ff00;
    }
    
    .delete-btn:hover {
        background-color: #005500;
    }
    
    /* Ensure menu items with buttons are properly styled */
    .menu-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    </style>
    """
    
    return base_template("TradeArena Web Terminal - Manage Views", content, 
                        additional_js=additional_js, additional_css=additional_css)
