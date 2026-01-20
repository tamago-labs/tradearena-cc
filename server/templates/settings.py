"""
Settings page templates for TradeArena Web Terminal
"""

from ..static import SUBMENU_JS
from .base import base_template

def settings_template(config: dict = None) -> str:
    """Settings page template with Walrus and Web Search configuration"""
    if config is None:
        config = {
            "walrus": {
                "enabled": False
            },
            "web_search": {
                "enabled": False
            }
        }
    
    walrus_config = config.get("walrus", {})
    web_search_config = config.get("web_search", {})
    
    additional_css = """
.settings-container {
    max-width: 600px;
    margin: 0 auto;
}
.settings-section {
    border: 2px solid #00ff00;
    padding: 20px;
    background: rgba(0, 255, 0, 0.05);
    margin: 20px 0;
}
.section-header {
    color: #00ff00;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 15px;
    border-bottom: 1px solid #00ff00;
    padding-bottom: 10px;
}
.section-description {
    color: #cccccc;
    font-size: 14px;
    margin-bottom: 20px;
    line-height: 1.4;
}
.form-field {
    margin: 15px 0;
}
.checkbox-field {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 20px 0;
}
.checkbox-input {
    width: auto;
    margin: 0;
}
.checkbox-label {
    color: #00cc00;
    font-weight: bold;
    font-size: 16px;
    margin: 0;
}
.form-label {
    color: #00cc00;
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
}
.form-input {
    width: 100%;
    background: #000000;
    border: 1px solid #00ff00;
    color: #ffffff;
    padding: 10px;
    font-family: inherit;
    font-size: 14px;
    box-sizing: border-box;
}
.form-input:focus {
    outline: none;
    border-color: #00cc00;
    box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
}
.form-input:disabled {
    background: #222222;
    color: #666666;
    border-color: #444444;
}
.help-text {
    font-size: 12px;
    color: #888888;
    margin-top: 5px;
    font-style: italic;
}
.walrus-config-fields {
    background: rgba(0, 100, 0, 0.1);
    padding: 15px;
    border-radius: 5px;
    border-left: 3px solid #00ff00;
    margin-top: 15px;
}
.highlight-text {
    color: #00ff00;
    font-weight: bold;
}
.setting-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 30px 0;
}
.setting-button {
    background: #000000;
    border: 2px solid #00ff00;
    color: #00ff00;
    padding: 12px 30px;
    font-family: inherit;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 5px;
    transition: all 0.3s ease;
    min-width: 150px;
    text-align: center;
}
.setting-button:hover {
    background: rgba(0, 255, 0, 0.1);
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}
.setting-button:active {
    transform: scale(0.98);
}
.setting-button.active {
    background: rgba(0, 255, 0, 0.3);
    border-color: #00ff00;
    color: #ffffff;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
}
.setting-button.inactive {
    background: #000000;
    border-color: #666666;
    color: #666666;
}
.setting-button.inactive:hover {
    background: rgba(100, 100, 100, 0.1);
    border-color: #888888;
    box-shadow: 0 0 5px rgba(136, 136, 136, 0.3);
}
    """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">TRADEARENA SETTINGS</div>
        </div>
        
        <div class="settings-container">
            <!-- Walrus Storage Section -->
            <div class="settings-section">
                <div class="section-header">Walrus Storage Configuration</div>
                
                <div class="section-description">
                    Enable Walrus decentralized storage to improve <span class="highlight-text">collective intelligence</span> 
                    by sharing trading decisions and performance data across all TradeArena agents.
                </div>
                
                <div class="setting-buttons">
                    <button id="walrus_enable" class="setting-button {'active' if walrus_config.get('enabled') else 'inactive'}" 
                            data-action="enable" data-setting="walrus">
                        ENABLE
                    </button>
                    <button id="walrus_disable" class="setting-button {'active' if not walrus_config.get('enabled') else 'inactive'}" 
                            data-action="disable" data-setting="walrus">
                        DISABLED
                    </button>
                </div>
            </div>
            
            <!-- Web Search Section -->
            <div class="settings-section">
                <div class="section-header">Web Search Configuration</div>
                
                <div class="section-description">
                    Enable <span class="highlight-text">internet search capability</span> 
                    to allow your agent to search the web for real-time market information, news, and research data.
                </div>
                
                <div class="setting-buttons">
                    <button id="websearch_enable" class="setting-button {'active' if web_search_config.get('enabled') else 'inactive'}" 
                            data-action="enable" data-setting="web_search">
                        ENABLE
                    </button>
                    <button id="websearch_disable" class="setting-button {'active' if not web_search_config.get('enabled') else 'inactive'}" 
                            data-action="disable" data-setting="web_search">
                        DISABLED
                    </button>
                </div>
            </div>
            
            <!-- Navigation Menu -->
            <div class="menu">
                <div class="menu-header">Settings Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="save-settings">Save Settings</div>
                    <div class="menu-item" data-action="reset-defaults">Reset to Defaults</div>
                    <div class="menu-item" data-action="back">Back to Main Menu</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Space to toggle checkboxes • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = f"""
{SUBMENU_JS}

class SettingsMenu extends SubMenu {{
    constructor() {{
        super();
        this.setupEventListeners();
        this.walrusEnabled = {walrus_config.get('enabled', False)};
        this.webSearchEnabled = {web_search_config.get('enabled', False)};
    }}
    
    setupEventListeners() {{
        // Walrus buttons
        const walrusEnableButton = document.getElementById('walrus_enable');
        const walrusDisableButton = document.getElementById('walrus_disable');
        
        walrusEnableButton.addEventListener('click', () => {{
            this.setWalrusEnabled(true);
        }});
        
        walrusDisableButton.addEventListener('click', () => {{
            this.setWalrusEnabled(false);
        }});
        
        // Web Search buttons
        const webSearchEnableButton = document.getElementById('websearch_enable');
        const webSearchDisableButton = document.getElementById('websearch_disable');
        
        webSearchEnableButton.addEventListener('click', () => {{
            this.setWebSearchEnabled(true);
        }});
        
        webSearchDisableButton.addEventListener('click', () => {{
            this.setWebSearchEnabled(false);
        }});
        
        // Allow Space/Enter keys when buttons are focused
        [
            walrusEnableButton, walrusDisableButton, 
            webSearchEnableButton, webSearchDisableButton
        ].forEach(button => {{
            button.addEventListener('keydown', (e) => {{
                if (e.code === 'Space' || e.code === 'Enter') {{
                    e.preventDefault();
                    button.click();
                }}
            }});
        }});
    }}
    
    setWalrusEnabled(enabled) {{
        this.walrusEnabled = enabled;
        this.updateWalrusButtons();
    }}
    
    setWebSearchEnabled(enabled) {{
        this.webSearchEnabled = enabled;
        this.updateWebSearchButtons();
    }}
    
    updateWalrusButtons() {{
        const enableButton = document.getElementById('walrus_enable');
        const disableButton = document.getElementById('walrus_disable');
        
        if (this.walrusEnabled) {{
            enableButton.className = 'setting-button active';
            disableButton.className = 'setting-button inactive';
        }} else {{
            enableButton.className = 'setting-button inactive';
            disableButton.className = 'setting-button active';
        }}
    }}
    
    updateWebSearchButtons() {{
        const enableButton = document.getElementById('websearch_enable');
        const disableButton = document.getElementById('websearch_disable');
        
        if (this.webSearchEnabled) {{
            enableButton.className = 'setting-button active';
            disableButton.className = 'setting-button inactive';
        }} else {{
            enableButton.className = 'setting-button inactive';
            disableButton.className = 'setting-button active';
        }}
    }}
    
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'save-settings':
                this.saveSettings();
                break;
            case 'reset-defaults':
                this.resetToDefaults();
                break;
            case 'back':
                window.location.href = '/';
                break;
        }}
    }}
    
    async saveSettings() {{
        // Collect form data
        const settings = {{
            walrus: {{
                enabled: this.walrusEnabled
            }},
            web_search: {{
                enabled: this.webSearchEnabled
            }}
        }};
        
        try {{
            const response = await fetch('/api/settings/save', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(settings)
            }});
            
            const result = await response.json();
            
            if (response.ok) {{
                let message = 'Settings saved successfully!\\\\n\\\\n';
                
                if (settings.walrus.enabled) {{
                    message += '• Walrus storage is now enabled. Your agent will contribute to collective intelligence.\\\\n';
                }} else {{
                    message += '• Walrus storage is disabled. Your agent will operate independently.\\\\n';
                }}
                
                if (settings.web_search.enabled) {{
                    message += '• Web search is now enabled. Your agent can search the internet for information.\\\\n';
                }} else {{
                    message += '• Web search is disabled. Your agent will use only provided data sources.\\\\n';
                }}
                
                alert(message);
            }} else {{
                alert('Failed to save settings: ' + (result.error || 'Unknown error'));
            }}
        }} catch (error) {{
            alert('Error saving settings: ' + error.message);
        }}
    }}
    
    async resetToDefaults() {{
        if (confirm('Are you sure you want to reset all settings to defaults? This action cannot be undone.')) {{
            try {{
                const response = await fetch('/api/settings/load');
                const result = await response.json();
                
                if (response.ok) {{
                    // Load defaults into form
                    const defaults = result.settings;
                    this.setWalrusEnabled(defaults.walrus.enabled);
                    this.setWebSearchEnabled(defaults.web_search.enabled);
                    
                    alert('Settings reset to defaults. Click "Save Settings" to apply.');
                }} else {{
                    alert('Failed to load defaults: ' + (result.error || 'Unknown error'));
                }}
            }} catch (error) {{
                alert('Error loading defaults: ' + error.message);
            }}
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new SettingsMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Settings", content, additional_css, additional_js)
