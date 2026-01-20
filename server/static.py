"""
Static assets for TradeArena Web Terminal
CSS and JavaScript components
"""

# Base CSS for retro terminal aesthetic
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: #000000;
    color: #00ff00;
    font-family: 'Courier Prime', 'Courier New', monospace;
    font-size: 16px;
    overflow: hidden;
    height: 100vh;
    position: relative;
}

/* Scanline effect */
body::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        transparent 50%,
        rgba(0, 255, 0, 0.03) 50%
    );
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 1;
}

/* CRT screen curve effect */
.crt {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    box-shadow: 
        inset 0 0 40px rgba(0, 255, 0, 0.1),
        inset 0 0 20px rgba(0, 0, 0, 0.8);
    pointer-events: none;
    z-index: 2;
}

.terminal {
    position: relative;
    z-index: 0;
    padding: 20px;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.terminal-header {
    border-bottom: 2px solid #00ff00;
    padding-bottom: 10px;
    margin-bottom: 20px;
    text-align: center;
}

.ascii-art {
    font-size: 12px;
    line-height: 1.2;
    color: #00ff00;
    text-shadow: 0 0 5px #00ff00;
    white-space: pre;
    margin-bottom: 10px;
}

.title {
    font-size: 24px;
    font-weight: bold;
    color: #00ff00;
    text-shadow: 0 0 10px #00ff00;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 14px;
    color: #00cc00;
    margin-bottom: 10px;
}

.menu-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.menu {
    border: 2px solid #00ff00;
    padding: 20px;
    background: rgba(0, 255, 0, 0.05);
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    min-width: 500px;
}

.menu-item {
    padding: 8px 0;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
}

.menu-item.selected {
    background: #00ff00;
    color: #000000;
    font-weight: bold;
    box-shadow: 0 0 10px #00ff00;
}

.menu-item.selected::before {
    content: "> ";
    position: absolute;
    left: -20px;
}

.menu-header {
    font-weight: bold;
    margin-bottom: 15px;
    text-align: center;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.instructions {
    margin-top: 20px;
    text-align: center;
    font-size: 12px;
    color: #00cc00;
    border-top: 1px solid #00ff00;
    padding-top: 10px;
}

.blink {
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}

.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 5px;
}

.status-indicator.online {
    background: #00ff00;
    box-shadow: 0 0 5px #00ff00;
}

.status-indicator.offline {
    background: #ff0000;
    box-shadow: 0 0 5px #ff0000;
}

.status-indicator.warning {
    background: #ffff00;
    box-shadow: 0 0 5px #ffff00;
}
"""

# JavaScript for keyboard navigation
MENU_JS = """
class TerminalMenu {
    constructor() {
        this.selectedIndex = 0;
        this.menuItems = document.querySelectorAll('.menu-item');
        this.currentMenu = 'main';
        this.init();
    }
    
    init() {
        this.updateSelection();
        this.bindEvents();
    }
    
    bindEvents() {
        // Remove existing listener to prevent duplicates
        if (this.keyHandler) {
            document.removeEventListener('keydown', this.keyHandler);
        }
        
        // Create bound handler
        this.keyHandler = (e) => {
            switch(e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    this.moveUp();
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.moveDown();
                    break;
                case 'Enter':
                    e.preventDefault();
                    this.select();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.goBack();
                    break;
            }
        };
        
        document.addEventListener('keydown', this.keyHandler);
    }
    
    moveUp() {
        this.selectedIndex = (this.selectedIndex - 1 + this.menuItems.length) % this.menuItems.length;
        this.updateSelection();
    }
    
    moveDown() {
        this.selectedIndex = (this.selectedIndex + 1) % this.menuItems.length;
        this.updateSelection();
    }
    
    updateSelection() {
        this.menuItems.forEach((item, index) => {
            item.classList.toggle('selected', index === this.selectedIndex);
        });
    }
    
    select() {
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {
            case 'interactive':
                window.location.href = '/interactive';
                break;
            case 'views':
                window.location.href = '/views';
                break;
            case 'manage-agents':
                window.location.href = '/manage-agents';
                break;
            case 'settings':
                window.location.href = '/settings';
                break;
        }
    }
    
    goBack() {
        // Always go back to main menu
        window.location.href = '/';
    }
}

// Initialize terminal menu when page loads
document.addEventListener('DOMContentLoaded', () => {
    new TerminalMenu();
});
"""

# JavaScript for sub-menus (interactive, views, etc.)
SUBMENU_JS = """
class SubMenu {
    constructor() {
        this.selectedIndex = 0;
        this.menuItems = document.querySelectorAll('.menu-item');
        this.init();
    }
    
    init() {
        this.updateSelection();
        this.bindEvents();
    }
    
    bindEvents() {
        // Remove existing listener to prevent duplicates
        if (this.keyHandler) {
            document.removeEventListener('keydown', this.keyHandler);
        }
        
        // Create bound handler
        this.keyHandler = (e) => {
            switch(e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    this.moveUp();
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.moveDown();
                    break;
                case 'Enter':
                    e.preventDefault();
                    this.select();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.goBack();
                    break;
            }
        };
        
        document.addEventListener('keydown', this.keyHandler);
    }
    
    moveUp() {
        this.selectedIndex = (this.selectedIndex - 1 + this.menuItems.length) % this.menuItems.length;
        this.updateSelection();
    }
    
    moveDown() {
        this.selectedIndex = (this.selectedIndex + 1) % this.menuItems.length;
        this.updateSelection();
    }
    
    updateSelection() {
        this.menuItems.forEach((item, index) => {
            item.classList.toggle('selected', index === this.selectedIndex);
        });
    }
    
    goBack() {
        window.location.href = '/';
    }
    
    select() {
        // This method should be overridden by specific menu implementations
        console.log('Select method should be overridden by subclass');
    }
}
"""
