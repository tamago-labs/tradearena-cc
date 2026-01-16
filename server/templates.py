"""
HTML templates for TradeArena Web Terminal
Template generation functions
"""

from .static import BASE_CSS, MENU_JS, SUBMENU_JS

# ASCII art for TRADE ARENA
TRADE_ARENA_ASCII = """
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.   .----------------.  .----------------.  .----------------.  .-----------------. .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || |  _______     | || |      __      | || |  ________    | || |  _________   | | | |      __      | || |  _______     | || |  _________   | || | ____  _____  | || |      __      | |
| | |  _   _  |  | || | |_   __ \    | || |     /  \     | || | |_   ___ `.  | || | |_   ___  |  | | | |     /  \     | || | |_   __ \    | || | |_   ___  |  | || ||_   \|_   _| | || |     /  \     | |
| | |_/ | | \_|  | || |   | |__) |   | || |    / /\ \    | || |   | |   `. \ | || |   | |_  \_|  | | | |    / /\ \    | || |   | |__) |   | || |   | |_  \_|  | || |  |   \ | |   | || |    / /\ \    | |
| |     | |      | || |   |  __ /    | || |   / ____ \   | || |   | |    | | | || |   |  _|  _   | | | |   / ____ \   | || |   |  __ /    | || |   |  _|  _   | || |  | |\ \| |   | || |   / ____ \   | |
| |    _| |_     | || |  _| |  \ \_  | || | _/ /    \ \_ | || |  _| |___.' / | || |  _| |___/ |  | | | | _/ /    \ \_ | || |  _| |  \ \_  | || |  _| |___/ |  | || | _| |_\   |_  | || | _/ /    \ \_ | |
| |   |_____|    | || | |____| |___| | || ||____|  |____|| || | |________.'  | || | |_________|  | | | ||____|  |____|| || | |____| |___| | || | |_________|  | || ||_____|\____| | || ||____|  |____|| |
| |              | || |              | || |              | || |              | || |              | | | |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'   '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""

def base_template(title: str, content: str, additional_css: str = "", additional_js: str = "") -> str:
    """Base template wrapper for all pages"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{BASE_CSS}
{additional_css}
    </style>
</head>
<body>
    <div class="crt"></div>
    <div class="terminal">
        {content}
    </div>
    <script>
{additional_js}
    </script>
</body>
</html>"""

def main_page_template() -> str:
    """Main menu page template"""
    content = f"""
        <div class="terminal-header">
            <div class="ascii-art">{TRADE_ARENA_ASCII}</div>
            <div class="title">Your Vibe Trading Arena for AI Agents</div>
            <div class="subtitle">Cronos · Sui · Walrus — v1.0.0</div>
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
                    <div class="menu-item" data-action="config">
                        <span class="status-indicator warning"></span>Configure Agent
                    </div>
                    <div class="menu-item" data-action="walrus">
                        <span class="status-indicator online"></span>Walrus Settings
                    </div>
                    <div class="menu-item" data-action="logs">
                        <span class="status-indicator online"></span>Agent Logs
                    </div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    return base_template("TradeArena Terminal", content, additional_js=MENU_JS)

def interactive_mode_template() -> str:
    """Interactive mode page template"""
    content = """
        <div class="terminal-header">
            <div class="title">INTERACTIVE MODE</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">Select Session Type</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="new">Start New Session</div>
                    <div class="menu-item" data-action="resume">Resume Last Session</div>
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

class InteractiveMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'new':
                alert('Starting new session... This would launch the trading agent interface.');
                break;
            case 'resume':
                alert('Resuming last session... This would restore previous trading state.');
                break;
            case 'back':
                window.location.href = '/';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new InteractiveMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Interactive Mode", content, additional_js=additional_js)

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

def config_page_template() -> str:
    """Configure agent page template"""
    additional_css = """
.status-text {
    font-size: 12px;
    color: #ffff00;
}
    """
    
    content = """
        <div class="terminal-header">
            <div class="title">CONFIGURE AGENT</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">Configuration Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="ai-model">
                        AI Model <span class="status-text">[Not Configured]</span>
                    </div>
                    <div class="menu-item" data-action="trading-chains">
                        Trading Chains <span class="status-text">[Cronos, KAIA]</span>
                    </div>
                    <div class="menu-item" data-action="risk-management">
                        Risk Management <span class="status-text">[Enabled]</span>
                    </div>
                    <div class="menu-item" data-action="api-keys">
                        API Keys <span class="status-text">[Partially Configured]</span>
                    </div>
                    <div class="menu-item" data-action="notifications">
                        Notifications <span class="status-text">[Disabled]</span>
                    </div>
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

class ConfigMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'ai-model':
                alert('AI Model Configuration - This would open the AI provider setup');
                break;
            case 'trading-chains':
                alert('Trading Chains Configuration - This would open chain selection');
                break;
            case 'risk-management':
                alert('Risk Management Settings - This would open risk parameters');
                break;
            case 'api-keys':
                alert('API Keys Configuration - This would open secure key management');
                break;
            case 'notifications':
                alert('Notification Settings - This would open alert configuration');
                break;
            case 'back':
                window.location.href = '/';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new ConfigMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Configure Agent", content, additional_css, additional_js)

def walrus_page_template() -> str:
    """Walrus settings page template"""
    additional_css = """
.content-area {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.walrus-info {
    border: 2px solid #00ff00;
    padding: 30px;
    background: rgba(0, 255, 0, 0.05);
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    min-width: 600px;
    text-align: center;
}

.walrus-icon {
    font-size: 48px;
    margin-bottom: 20px;
}

.status {
    font-size: 18px;
    margin: 10px 0;
}

.status.online {
    color: #00ff00;
}

.endpoint {
    font-size: 14px;
    color: #00cc00;
    margin: 5px 0;
}

.actions {
    margin-top: 30px;
}

.action-btn {
    background: #00ff00;
    color: #000000;
    border: 2px solid #00ff00;
    padding: 10px 20px;
    margin: 0 10px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
}

.action-btn:hover {
    background: #000000;
    color: #00ff00;
}
    """
    
    content = """
        <div class="terminal-header">
            <div class="title">WALRUS SETTINGS</div>
        </div>
        
        <div class="content-area">
            <div class="walrus-info">
                <div class="walrus-icon">🐋</div>
                <div class="status online">● WALRUS STORAGE: ONLINE</div>
                <div class="endpoint">Endpoint: https://walrus.ai</div>
                <div class="endpoint">Publisher: publisher.walrus.ai</div>
                <div class="endpoint">Status: Connected and Syncing</div>
                
                <div class="actions">
                    <button class="action-btn" onclick="alert('Testing Walrus connection...')">Test Connection</button>
                    <button class="action-btn" onclick="alert('Configuring Walrus settings...')">Configure</button>
                    <button class="action-btn" onclick="window.location.href='/'">Back to Menu</button>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Press Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = """
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        window.location.href = '/';
    }
});
    """
    
    return base_template("TradeArena Web Terminal - Walrus Settings", content, additional_css, additional_js)

def logs_page_template() -> str:
    """Agent logs page template"""
    additional_css = """
.logs-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    border: 2px solid #00ff00;
    background: rgba(0, 255, 0, 0.05);
    padding: 15px;
    overflow: hidden;
}

.logs-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #00ff00;
}

.log-level {
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: bold;
}

.log-level.info { background: #00ff00; color: #000000; }
.log-level.warn { background: #ffff00; color: #000000; }
.log-level.error { background: #ff0000; color: #ffffff; }
.log-level.debug { background: #00ccff; color: #000000; }

.logs-content {
    flex: 1;
    overflow-y: auto;
    font-size: 12px;
    line-height: 1.4;
}

.log-entry {
    margin: 2px 0;
    padding: 2px 0;
    white-space: pre-wrap;
    word-break: break-all;
}

.log-time {
    color: #00cc00;
    margin-right: 10px;
}

.log-message {
    color: #00ff00;
}

.log-message.error {
    color: #ff0000;
}

.log-message.warn {
    color: #ffff00;
}

.log-message.debug {
    color: #00ccff;
}

.controls {
    margin-top: 20px;
    text-align: center;
}

.control-btn {
    background: #00ff00;
    color: #000000;
    border: 2px solid #00ff00;
    padding: 8px 16px;
    margin: 0 5px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
}

.control-btn:hover {
    background: #000000;
    color: #00ff00;
}
    """
    
    content = """
        <div class="terminal-header">
            <div class="title">AGENT LOGS</div>
        </div>
        
        <div class="logs-container">
            <div class="logs-header">
                <span>Live Agent Activity Log</span>
                <span class="log-level info">LIVE</span>
            </div>
            
            <div class="logs-content" id="logsContent">
                <div class="log-entry">
                    <span class="log-time">10:45:12</span>
                    <span class="log-message info">[INFO] TradeArena Agent System initialized</span>
                </div>
                <div class="log-entry">
                    <span class="log-time">10:45:13</span>
                    <span class="log-message info">[INFO] Connecting to Cronos blockchain...</span>
                </div>
                <div class="log-entry">
                    <span class="log-time">10:45:14</span>
                    <span class="log-message info">[INFO] Successfully connected to Cronos RPC</span>
                </div>
                <div class="log-entry">
                    <span class="log-time">10:45:15</span>
                    <span class="log-message info">[INFO] Connecting to KAIA blockchain...</span>
                </div>
                <div class="log-entry">
                    <span class="log-time">10:45:16</span>
                    <span class="log-message warn">[WARN] High gas fees detected on KAIA network</span>
                </div>
                <div class="log-entry">
                    <span class="log-time">10:45:17</span>
                    <span class="log-message info">[INFO] Market scanner started</span>
                </div>
                <div class="log-entry">
                    <span class="log-time">10:45:18</span>
                    <span class="log-message info">[INFO] Scanning for arbitrage opportunities...</span>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button class="control-btn" onclick="clearLogs()">Clear Logs</button>
            <button class="control-btn" onclick="togglePause()">Pause</button>
            <button class="control-btn" onclick="exportLogs()">Export</button>
            <button class="control-btn" onclick="window.location.href='/'">Back to Menu</button>
        </div>
        
        <div class="instructions">
            Press Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = """
let isPaused = false;
let logIndex = 28;

function addLog() {
    if (isPaused) return;
    
    const logsContent = document.getElementById('logsContent');
    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    
    const messages = [
        { type: 'info', text: '[INFO] Scanning market conditions...' },
        { type: 'debug', text: '[DEBUG] Checking liquidity pools...' },
        { type: 'info', text: '[INFO] Monitoring price movements...' },
        { type: 'warn', text: '[WARN] Volatility increasing in DeFi markets' },
        { type: 'info', text: '[INFO] AI model analyzing market sentiment...' },
        { type: 'debug', text: '[DEBUG] Updating portfolio metrics...' }
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.innerHTML = `
        <span class="log-time">${time}</span>
        <span class="log-message ${randomMessage.type}">${randomMessage.text}</span>
    `;
    
    logsContent.appendChild(logEntry);
    logsContent.scrollTop = logsContent.scrollHeight;
    
    // Limit logs to last 50 entries
    const entries = logsContent.querySelectorAll('.log-entry');
    if (entries.length > 50) {
        entries[0].remove();
    }
}

function clearLogs() {
    const logsContent = document.getElementById('logsContent');
    logsContent.innerHTML = '<div class="log-entry"><span class="log-time">' + 
        new Date().toTimeString().split(' ')[0] + 
        '</span><span class="log-message info">[INFO] Logs cleared</span></div>';
}

function togglePause() {
    isPaused = !isPaused;
    event.target.textContent = isPaused ? 'Resume' : 'Pause';
}

function exportLogs() {
    alert('Exporting logs to file... (This would download a log file)');
}

// Simulate live log updates
setInterval(addLog, 3000);

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        window.location.href = '/';
    }
});
    """
    
    return base_template("TradeArena Web Terminal - Agent Logs", content, additional_css, additional_js)