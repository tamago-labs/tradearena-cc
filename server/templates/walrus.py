"""
Walrus settings templates for TradeArena Web Terminal
"""

from ..static import SUBMENU_JS
from .base import base_template

def walrus_settings_template(config: dict = None) -> str:
    """Walrus settings page template"""
    if config is None:
        config = {
            "endpoint": "https://walrus-testnet.walrus.ai",
            "publisher_url": "https://publisher.walrus.ai", 
            "aggregator_url": "https://aggregator.walrus.ai",
            "enabled": True
        }
    
    additional_css = """
.config-form {
    border: 2px solid #00ff00;
    padding: 20px;
    background: rgba(0, 255, 0, 0.05);
    margin: 10px auto;
    max-width: 500px;
}
.form-field {
    margin: 15px 0;
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
    padding: 8px;
    font-family: inherit;
    font-size: 14px;
}
.form-input:focus {
    outline: none;
    border-color: #00cc00;
    box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
}
.checkbox-field {
    display: flex;
    align-items: center;
    gap: 10px;
}
.checkbox-input {
    width: auto;
    margin: 0;
}
.help-text {
    font-size: 11px;
    color: #888888;
    margin-top: 5px;
    font-style: italic;
}
    """
    
    endpoint_value = config.get('endpoint', '')
    publisher_value = config.get('publisher_url', '')
    aggregator_value = config.get('aggregator_url', '')
    enabled_checked = 'checked' if config.get('enabled') else ''
    
    content = f"""
        <div class="terminal-header">
            <div class="title">WALRUS SETTINGS</div>
        </div>
        
        <div class="menu-container">
            <div class="config-form">
                <div class="form-field checkbox-field">
                    <input type="checkbox" id="enabled" class="form-input checkbox-input" {enabled_checked} />
                    <label for="enabled" class="form-label" style="margin: 0;">Enable Walrus Storage</label>
                </div>
                
                <div class="form-field">
                    <label for="endpoint" class="form-label">Walrus Endpoint:</label>
                    <input type="text" id="endpoint" class="form-input" value="{endpoint_value}" />
                    <div class="help-text">Walrus network endpoint for data storage</div>
                </div>
                
                <div class="form-field">
                    <label for="publisher_url" class="form-label">Publisher URL:</label>
                    <input type="text" id="publisher_url" class="form-input" value="{publisher_value}" />
                    <div class="help-text">URL for publishing data to Walrus network</div>
                </div>
                
                <div class="form-field">
                    <label for="aggregator_url" class="form-label">Aggregator URL:</label>
                    <input type="text" id="aggregator_url" class="form-input" value="{aggregator_value}" />
                    <div class="help-text">URL for Walrus aggregator service</div>
                </div>
            </div>
            
            <div class="menu">
                <div class="menu-header">Configuration Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="test-connection">Test Connection</div>
                    <div class="menu-item" data-action="save-settings">Save Settings</div>
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

class WalrusSettingsMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'test-connection':
                this.testConnection();
                break;
            case 'save-settings':
                this.saveSettings();
                break;
            case 'back':
                window.location.href = '/';
                break;
        }}
    }}
    
    async testConnection() {{
        // Get current form values
        const enabled = document.getElementById('enabled').checked;
        const endpoint = document.getElementById('endpoint').value.trim();
        
        if (!enabled) {{
            alert('Walrus storage is disabled. Enable it to test connection.');
            return;
        }}
        
        if (!endpoint) {{
            alert('Please enter a Walrus endpoint URL.');
            return;
        }}
        
        try {{
            const response = await fetch('/api/walrus/test', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    endpoint: endpoint
                }})
            }});
            
            const result = await response.json();
            
            if (response.ok) {{
                alert(`Connection successful!\\\\nLatency: ${{result.latency}}ms\\\\nStatus: ${{result.status}}`);
            }} else {{
                alert(`Connection failed: ${{result.error}}`);
            }}
        }} catch (error) {{
            alert(`Connection error: ${{error.message}}`);
        }}
    }}
    
    async saveSettings() {{
        // Collect form data
        const settings = {{
            enabled: document.getElementById('enabled').checked,
            endpoint: document.getElementById('endpoint').value.trim(),
            publisher_url: document.getElementById('publisher_url').value.trim(),
            aggregator_url: document.getElementById('aggregator_url').value.trim()
        }};
        
        try {{
            const response = await fetch('/api/walrus/save', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(settings)
            }});
            
            const result = await response.json();
            
            if (response.ok) {{
                alert('Walrus settings saved successfully!');
            }} else {{
                alert(`Failed to save settings: ${{result.error}}`);
            }}
        }} catch (error) {{
            alert(`Error saving settings: ${{error.message}}`);
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new WalrusSettingsMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Walrus Settings", content, additional_css, additional_js)
