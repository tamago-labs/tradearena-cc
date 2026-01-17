"""
HTML templates for TradeArena Web Terminal
Template generation functions
"""

from .static import BASE_CSS, MENU_JS, SUBMENU_JS

# ASCII art for TRADE ARENA
TRADE_ARENA_ASCII = r"""
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
                    <div class="menu-item" data-action="walrus">
                        <span class="status-indicator online"></span>Walrus Settings
                    </div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    return base_template("TradeArena Terminal", content, additional_js=MENU_JS)

def manage_agents_template(agents: list = None) -> str:
    """Manage agents page template"""
    additional_css = """
.agent-info {
    font-size: 12px;
    color: #00cc00;
    margin-left: 10px;
}
.agent-details {
    font-size: 11px;
    color: #888888;
    margin-left: 20px;
}
.empty-state { 
    color: #888888;
    font-style: italic; 
}
.menu-item.selected .agent-info {
    color: #000000;
}
.menu-item.selected .session-info {
    color: #00cc00;
}
    """
    
    # Generate agent menu items dynamically
    agent_items = ""
    if agents and len(agents) > 0:
        for agent in agents:
            agent_items += f"""
                    <div class="menu-item" data-action="agent-{agent['id']}">
                        {agent['name']} <span class="agent-info">[{agent['ai_provider'].replace('_', ' ').title()} | {agent['trading_chain'].title()}]</span>
                    </div>
            """
    else:
        agent_items = """
                    <div class="menu-item" data-action="no-agents">
                        <span class="empty-state" style="color: #888888 !important; font-style: italic !important; text-align: center !important; display: block !important;">No agents available. Create an agent first.</span>
                    </div>
        """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">MANAGE AGENTS</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">Agent Configurations</div>
                <div id="menuItems">
{agent_items}
                    <div class="menu-item" data-action="create-new">
                        + Create New Agent
                    </div>
                    <div class="menu-item" data-action="back">Back to Main Menu</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    # Generate dynamic JavaScript
    agent_js_cases = ""
    if agents and len(agents) > 0:
        for agent in agents:
            agent_js_cases += f"""
            case 'agent-{agent['id']}':
                window.location.href = '/manage-agent/{agent['id']}';
                break;
            """
    
    additional_js = f"""
{SUBMENU_JS}

class ManageAgentsMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
{agent_js_cases}
            case 'no-agents':
                // Do nothing - just a placeholder
                break;
            case 'create-new':
                window.location.href = '/create-agent';
                break;
            case 'back':
                window.location.href = '/';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new ManageAgentsMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Manage Agents", content, additional_css, additional_js)

def manage_agent_template(agent_id: str, agent_data: dict = None) -> str:
    """Manage individual agent page template"""
    if agent_data is None:
        agent_data = {
            "name": "Agent #1",
            "ai_provider": "anthropic",
            "trading_chain": "cronos"
        }
    
    additional_css = """
.agent-details {
    border: 2px solid #00ff00;
    padding: 20px;
    background: rgba(0, 255, 0, 0.05);
    margin: 20px 0;
}
.detail-row {
    margin: 10px 0;
    display: flex;
    justify-content: space-between;
}
.detail-label {
    color: #00cc00;
    font-weight: bold;
}
.detail-value {
    color: #ffffff;
}
    """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">MANAGE AGENT - {agent_data['name']}</div>
        </div>
        
        <div class="menu-container">
            <div class="agent-details">
                <div class="detail-row">
                    <span class="detail-label">Agent ID:</span>
                    <span class="detail-value">{agent_id}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Name:</span>
                    <span class="detail-value">{agent_data['name']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">AI Provider:</span>
                    <span class="detail-value">{agent_data['ai_provider']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Trading Chain:</span>
                    <span class="detail-value">{agent_data['trading_chain']}</span>
                </div>
            </div>
            
            <div class="menu">
                <div class="menu-header">Agent Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="delete-agent">Delete Agent</div>
                    <div class="menu-item" data-action="back">Back to Agent List</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = f"""
{SUBMENU_JS}

class ManageAgentMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'delete-agent':
                if (confirm('Are you sure you want to delete this agent?')) {{
                    window.location.href = '/delete-agent/{agent_id}';
                }}
                break;
            case 'back':
                window.location.href = '/manage-agents';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new ManageAgentMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Manage Agent", content, additional_css, additional_js)

def create_agent_template() -> str:
    """Create new agent page template"""
    additional_css = """
.step-info {
    color: #00cc00;
    font-size: 14px;
    margin: 5px auto;
    text-align: center;
    font-weight: bold;
    display: block;
    width: 100%;
}
    """
    
    content = """
        <div class="terminal-header">
            <div class="title">CREATE NEW AGENT</div>
        </div>
        
        <div class="menu-container">
            <div class="step-info">Step 1: Select AI Provider</div>
            <div class="menu">
                <div class="menu-header">AI Provider</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="amazon-bedrock">Amazon Bedrock</div>
                    <div class="menu-item" data-action="anthropic">Anthropic</div>
                    <div class="menu-item" data-action="gemini">Gemini</div>
                    <div class="menu-item" data-action="openai-compatible">OpenAI Compatible</div>
                    <div class="menu-item" data-action="back">Back to Agent List</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = f"""
{SUBMENU_JS}

class CreateAgentMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'amazon-bedrock':
            case 'anthropic':
            case 'gemini':
            case 'openai-compatible':
                window.location.href = '/create-agent/config?provider=' + action;
                break;
            case 'back':
                window.location.href = '/manage-agents';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new CreateAgentMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Create Agent", content, additional_css, additional_js)

def create_agent_config_template(provider: str) -> str:
    """Create agent configuration page template"""
    from .agents import PROVIDER_CONFIGS
    
    provider_config = PROVIDER_CONFIGS.get(provider.replace("-", "_"), {})
    display_name = provider_config.get("display_name", provider.title())
    
    additional_css = """
.step-info {
    color: #00cc00;
    font-size: 14px;
    margin: 5px auto;
    text-align: center;
    font-weight: bold;
    display: block;
    width: 100%;
}
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
.credentials-help {
    border: 1px solid #ffff00;
    padding: 10px;
    margin: 10px 0;
    background: rgba(255, 255, 0, 0.05);
    font-size: 12px;
    color: #ffff00;
}
.credentials-help h4 {
    margin: 0 0 5px 0;
    color: #ffff00;
}
.credentials-help p {
    margin: 3px 0;
}
    """
    
    # Generate form fields based on provider configuration
    form_fields = ""
    
    if provider == "amazon-bedrock":
        form_fields = f"""
                    <div class="form-field">
                        <label class="form-label">Model ID:</label>
                        <input type="text" class="form-input" id="model_id" value="{provider_config['defaults']['model_id']}" />
                    </div>
                    <div class="form-field">
                        <label class="form-label">Region Name:</label>
                        <input type="text" class="form-input" id="region_name" value="{provider_config['defaults']['region_name']}" />
                    </div>
                    
                    <div class="credentials-help">
                        <h4>📋 AWS Credentials Setup:</h4>
                        <p>• Set AWS_ACCESS_KEY_ID environment variable</p>
                        <p>• Set AWS_SECRET_ACCESS_KEY environment variable</p>
                        <p>• Or configure AWS CLI profile</p>
                        <p>📖 <a href="https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/amazon-bedrock/" target="_blank" style="color: #ffff00;">Amazon Bedrock Setup Guide</a></p>
                    </div>
        """
    elif provider == "anthropic":
        form_fields = f"""
                    <div class="form-field">
                        <label class="form-label">API Key:</label>
                        <input type="password" class="form-input" id="api_key" placeholder="sk-ant-..." />
                    </div>
                    <div class="form-field">
                        <label class="form-label">Model ID:</label>
                        <input type="text" class="form-input" id="model_id" value="{provider_config['defaults']['model_id']}" />
                    </div>
                    
                    <div class="credentials-help">
                        <h4>📋 API Key Setup:</h4>
                        <p>• Get your API key from platform.claude.com</p>
                        <p>• Ensure you have sufficient credits</p>
                        <p>• API keys should start with "sk-ant-"</p>
                    </div>
        """
    elif provider == "gemini":
        form_fields = f"""
                    <div class="form-field">
                        <label class="form-label">API Key:</label>
                        <input type="password" class="form-input" id="api_key" placeholder="AIzaSy..." />
                    </div>
                    <div class="form-field">
                        <label class="form-label">Model ID:</label>
                        <input type="text" class="form-input" id="model_id" value="{provider_config['defaults']['model_id']}" />
                    </div>
                    
                    <div class="credentials-help">
                        <h4>📋 API Key Setup:</h4>
                        <p>• Get your API key from ai.google.dev</p>
                        <p>• Enable Gemini API in your Google Cloud project</p>
                        <p>• API keys should start with "AIzaSy"</p>
                    </div>
        """
    elif provider == "openai-compatible":
        placeholder = provider_config.get("placeholders", {}).get("base_url", "")
        form_fields = f"""
                    <div class="form-field">
                        <label class="form-label">API Key:</label>
                        <input type="password" class="form-input" id="api_key" placeholder="sk-..." />
                    </div>
                    <div class="form-field">
                        <label class="form-label">Base URL (Optional):</label>
                        <input type="text" class="form-input" id="base_url" placeholder="{placeholder}" />
                    </div>
                    <div class="form-field">
                        <label class="form-label">Model ID:</label>
                        <input type="text" class="form-input" id="model_id" value="{provider_config['defaults']['model_id']}" />
                        <small style="color: #888888;">💡 Examples: GLM-4.6, DeepSeek-R1, etc.</small>
                    </div>
                    
                    <div class="credentials-help">
                        <h4>📋 Compatible Servers:</h4>
                        <p>• OpenAI: Leave Base URL blank</p>
                        <p>• GLM-4.6: https://api.z.ai/api/coding/paas/v4</p>
                        <p>• DeepSeek-R1: https://api.deepseek.com/v1</p>
                    </div>
        """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">CREATE NEW AGENT</div>
        </div>
        
        <div class="menu-container">
            <div class="step-info">Step 2: Configure {display_name}</div>
            
            <div class="config-form">
{form_fields}
            </div>
            
            <div class="menu">
                <div class="menu-header">Configuration Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="continue">Continue to Trading Chain</div>
                    <div class="menu-item" data-action="back">Back to Provider Selection</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = f"""
{SUBMENU_JS}

class CreateAgentConfigMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'continue':
                // Collect form data
                const formData = {{}};
                const inputs = document.querySelectorAll('.form-input');
                inputs.forEach(input => {{
                    if (input.value.trim()) {{
                        formData[input.id] = input.value.trim();
                    }}
                }});
                
                // Build URL with parameters
                const params = new URLSearchParams();
                params.append('provider', '{provider}');
                Object.keys(formData).forEach(key => {{
                    params.append(key, formData[key]);
                }});
                
                window.location.href = '/create-agent/step2?' + params.toString();
                break;
            case 'back':
                window.location.href = '/create-agent';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new CreateAgentConfigMenu();
}});
    """
    
    return base_template(f"TradeArena Web Terminal - Configure {display_name}", content, additional_css, additional_js)

def create_agent_step2_template(ai_provider: str, config_params: dict = None) -> str:
    """Create agent step 2 - select trading chain"""
    additional_css = """
.step-info {
    color: #00cc00;
    font-size: 14px;
    margin: 5px auto;
    text-align: center;
    font-weight: bold;
    display: block;
    width: 100%;
}
.provider-info {
    color: #ffff00;
    font-size: 12px;
    text-align: center;
    margin: 3px auto;
    display: block;
    width: 100%;
}
.config-summary {
    border: 1px solid #00cc00;
    padding: 10px;
    margin: 10px auto;
    max-width: 400px;
    font-size: 11px;
    color: #888888;
}
    """
    
    provider_names = {
        "amazon-bedrock": "Amazon Bedrock",
        "anthropic": "Anthropic",
        "gemini": "Gemini",
        "openai-compatible": "OpenAI Compatible"
    }
    
    # Build configuration summary
    config_summary = ""
    if config_params:
        config_lines = []
        if "model_id" in config_params:
            config_lines.append(f"Model: {config_params['model_id']}")
        if "api_key" in config_params:
            config_lines.append(f"API Key: {'*' * 8}...{config_params['api_key'][-4:] if len(config_params['api_key']) > 4 else '****'}")
        if "region_name" in config_params:
            config_lines.append(f"Region: {config_params['region_name']}")
        if "base_url" in config_params and config_params["base_url"]:
            config_lines.append(f"Base URL: {config_params['base_url']}")
        
        if config_lines:
            config_summary = f"""
            <div class="config-summary">
                <div style="color: #00cc00; font-weight: bold; margin-bottom: 5px;">Configuration Summary:</div>
                {'<br>'.join(config_lines)}
            </div>
            """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">CREATE NEW AGENT</div>
        </div>
        
        <div class="menu-container">
            <div class="step-info">Step 3: Select Trading Chain</div>
            <div class="provider-info">AI Provider: {provider_names.get(ai_provider, ai_provider)}</div>
            {config_summary}
            <div class="menu">
                <div class="menu-header">Trading Chain</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="cronos">Cronos</div>
                    <div class="menu-item" data-action="kaia">Kaia</div>
                    <div class="menu-item" data-action="sui">Sui</div>
                    <div class="menu-item" data-action="back">Back</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    # Build URL parameters for navigation
    config_params_str = ""
    if config_params:
        from urllib.parse import urlencode
        config_params_str = "&" + urlencode(config_params)
    
    additional_js = f"""
{SUBMENU_JS}

class CreateAgentStep2Menu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'cronos':
            case 'kaia':
            case 'sui':
                window.location.href = '/create-agent/confirm?provider={ai_provider}&chain=' + action + '{config_params_str}';
                break;
            case 'back':
                window.location.href = '/create-agent/config?provider={ai_provider}';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new CreateAgentStep2Menu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Create Agent Step 3", content, additional_css, additional_js)

def create_agent_confirm_template(ai_provider: str, trading_chain: str, config_params: dict = None) -> str:
    """Create agent confirmation page"""
    additional_css = """
.step-info {
    color: #00cc00;
    font-size: 14px;
    margin: 5px auto;
    text-align: center;
    font-weight: bold;
    display: block;
    width: 100%;
}
.confirm-info {
    border: 2px solid #00ff00;
    padding: 15px;
    background: rgba(0, 255, 0, 0.05);
    margin: 10px auto;
    max-width: 400px;
}
.confirm-row {
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
}
.confirm-label {
    color: #00cc00;
    font-weight: bold;
}
.confirm-value {
    color: #ffffff;
}
.config-details {
    border: 1px solid #00cc00;
    padding: 10px;
    margin: 10px auto;
    max-width: 400px;
    font-size: 11px;
    color: #888888;
}
    """
    
    provider_names = {
        "amazon-bedrock": "Amazon Bedrock",
        "anthropic": "Anthropic", 
        "gemini": "Gemini",
        "openai-compatible": "OpenAI Compatible"
    }
    
    chain_names = {
        "cronos": "Cronos",
        "kaia": "Kaia",
        "sui": "Sui", 
        "aptos": "Aptos"
    }
    
    # Build configuration details
    config_details = ""
    if config_params:
        config_lines = []
        if "model_id" in config_params:
            config_lines.append(f"Model: {config_params['model_id']}")
        if "api_key" in config_params:
            config_lines.append(f"API Key: {'*' * 8}...{config_params['api_key'][-4:] if len(config_params['api_key']) > 4 else '****'}")
        if "region_name" in config_params:
            config_lines.append(f"Region: {config_params['region_name']}")
        if "base_url" in config_params and config_params["base_url"]:
            config_lines.append(f"Base URL: {config_params['base_url']}")
        
        if config_lines:
            config_details = f"""
            <div class="config-details">
                <div style="color: #00cc00; font-weight: bold; margin-bottom: 5px;">Provider Configuration:</div>
                {'<br>'.join(config_lines)}
            </div>
            """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">CREATE NEW AGENT</div>
        </div>
        
        <div class="menu-container">
            <div class="step-info">Confirm Agent Configuration</div>
            <div class="confirm-info">
                <div class="confirm-row">
                    <span class="confirm-label">AI Provider:</span>
                    <span class="confirm-value">{provider_names.get(ai_provider, ai_provider)}</span>
                </div>
                <div class="confirm-row">
                    <span class="confirm-label">Trading Chain:</span>
                    <span class="confirm-value">{chain_names.get(trading_chain, trading_chain)}</span>
                </div>
            </div>
            {config_details}
            
            <div class="menu">
                <div class="menu-header">Confirm Creation</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="confirm-create">Confirm</div>
                    <div class="menu-item" data-action="back">Back</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    # Build URL parameters for confirmation
    config_params_str = ""
    if config_params:
        from urllib.parse import urlencode
        config_params_str = "&" + urlencode(config_params)
    
    additional_js = f"""
{SUBMENU_JS}

class CreateAgentConfirmMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
            case 'confirm-create':
                window.location.href = '/create-agent/final?provider={ai_provider}&chain={trading_chain}{config_params_str}';
                break;
            case 'back':
                window.location.href = '/create-agent/step2?provider={ai_provider}{config_params_str}';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new CreateAgentConfirmMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Create Agent Confirm", content, additional_css, additional_js)

def interactive_mode_template() -> str:
    """Interactive mode page template"""
    additional_css = """
.session-info {
    font-size: 12px;
    color: #00cc00;
    margin-left: 10px;
}
.session-details {
    font-size: 11px;
    color: #888888;
    margin-left: 20px;
}
.loading {
    color: #ffff00;
    text-align: center;
    font-style: italic;
}
.empty-state { 
    color: #888888;
    font-style: italic; 
}
.menu-item .empty-state { 
    color: #888888 !important;
    font-style: italic !important;
    display: block !important;
}
.menu-item.selected .session-info {
    color: #000000 !important;
}
    """
    
    content = """
        <div class="terminal-header">
            <div class="title">INTERACTIVE MODE</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">Session Options</div>
                <div id="menuItems">
                    <div class="menu-item" data-action="new">Start New Session</div>
                    <div class="menu-item loading" id="loadingSessions">Loading recent sessions...</div>
                    <div id="sessionsList" style="display: none;">
                        <!-- Sessions will be loaded dynamically -->
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

class InteractiveMenu extends SubMenu {{
    constructor() {{
        super();
        this.loadSessions();
    }}
    
    async loadSessions() {{
        try {{
            const response = await fetch('/api/sessions');
            const data = await response.json();
            const sessions = data.sessions || [];
            
            const loadingItem = document.getElementById('loadingSessions');
            const sessionsList = document.getElementById('sessionsList');
            
            if (sessions.length === 0) {{
                loadingItem.innerHTML = '<span class="empty-state" style="color: #888888 !important; font-style: italic !important;">No previous sessions found</span>';
                loadingItem.classList.remove('loading');
                loadingItem.classList.add('empty-state');
                return;
            }}
            
            // Hide loading item
            loadingItem.style.display = 'none';
            
            // Create session items
            sessionsList.innerHTML = '';
            sessions.forEach(session => {{
                const sessionDate = new Date(session.updated_at).toLocaleDateString();
                const sessionTime = new Date(session.updated_at).toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
                const sessionSize = session.file_size || '0B';
                const agentInfo = session.agent_info || {{}};
                const providerDisplay = agentInfo.ai_provider_display || 'Unknown';
                const tradingChain = agentInfo.trading_chain || 'unknown';
                
                const sessionItem = document.createElement('div');
                sessionItem.className = 'menu-item';
                sessionItem.setAttribute('data-action', `session-${{session.session_id}}`);
                sessionItem.innerHTML = `
                    Resume Session [${{sessionDate}} ${{sessionTime}}] - ${{providerDisplay}} (${{tradingChain.charAt(0).toUpperCase() + tradingChain.slice(1)}}) [${{sessionSize}}]
                `;
                
                sessionsList.appendChild(sessionItem);
            }});
            
            sessionsList.style.display = 'block';
            
            // Reinitialize menu items
            this.menuItems = document.querySelectorAll('#menuItems .menu-item:not([style*="display: none"])');
            
        }} catch (error) {{
            console.error('Error loading sessions:', error);
            const loadingItem = document.getElementById('loadingSessions');
            loadingItem.textContent = 'Failed to load sessions';
            loadingItem.classList.remove('loading');
        }}
    }}
    
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        if (action.startsWith('session-')) {{
            const sessionId = action.replace('session-', '');
            window.location.href = `/resume-session/${{sessionId}}`;
            return;
        }}
        
        switch(action) {{
            case 'new':
                window.location.href = '/select-agent-for-session';
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
    
    return base_template("TradeArena Web Terminal - Interactive Mode", content, additional_css, additional_js)

def select_agent_for_session_template(agents: list = None) -> str:
    """Select agent for session template"""
    additional_css = """
.agent-info {
    font-size: 12px;
    color: #00cc00;
    margin-left: 10px;
}
.menu-item .empty-state { 
    color: #888888 !important;
    font-style: italic !important;
    display: block !important;
}
    """
    
    # Generate agent menu items dynamically
    agent_items = ""
    if agents and len(agents) > 0:
        for agent in agents:
            agent_items += f"""
                    <div class="menu-item" data-action="agent-{agent['id']}">
                        {agent['name']} <span class="agent-info">[{agent['ai_provider'].replace('_', ' ').title()} | {agent['trading_chain'].title()}]</span>
                    </div>
            """
    else:
        agent_items = """
                    <div class="menu-item" data-action="no-agents">
                        <span class="empty-state" style="color: #888888 !important; font-style: italic !important; display: block !important;">No agents available. Create an agent first.</span>
                    </div>
        """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">SELECT AGENT FOR SESSION</div>
        </div>
        
        <div class="menu-container">
            <div class="menu">
                <div class="menu-header">Choose Agent Configuration</div>
                <div id="menuItems">
{agent_items}
                    <div class="menu-item" data-action="back">Back to Interactive Mode</div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    # Generate dynamic JavaScript
    agent_js_cases = ""
    if agents and len(agents) > 0:
        for agent in agents:
            agent_js_cases += f"""
            case 'agent-{agent['id']}':
                window.location.href = '/chat-session/{agent['id']}';
                break;
            """
    
    additional_js = f"""
{SUBMENU_JS}

class SelectAgentForSessionMenu extends SubMenu {{
    select() {{
        const selectedItem = this.menuItems[this.selectedIndex];
        const action = selectedItem.getAttribute('data-action');
        
        switch(action) {{
{agent_js_cases}
            case 'no-agents':
                // Do nothing - just a placeholder
                break;
            case 'back':
                window.location.href = '/interactive';
                break;
        }}
    }}
}}

document.addEventListener('DOMContentLoaded', () => {{
    new SelectAgentForSessionMenu();
}});
    """
    
    return base_template("TradeArena Web Terminal - Select Agent for Session", content, additional_js=additional_js)

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

def chat_session_template(agent_id: str, agent_data: dict, session_id: str = None, messages: list = None) -> str:
    """Chat session template for interacting with AI agent"""
    
    # Generate preloaded messages HTML if provided
    preloaded_messages_html = ""
    if messages:
        for msg in messages:
            time_str = msg.get('created_at', '')
            if time_str:
                # Parse ISO format and format as time only
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    time_str = dt.strftime('%H:%M')
                except:
                    time_str = time_str[:8]  # Fallback to first 8 chars
            else:
                time_str = ""
            
            content = msg.get('content', '').replace('\n', '<br>')
            msg_class = msg.get('role', 'user')
            
            preloaded_messages_html += f"""
                <div class="message {msg_class}">
                    <span class="message-time">{time_str}:</span>
                    <span class="message-content">{content}</span>
                </div>
            """
    
    # Generate session_id JavaScript for URL building
    session_id_js = ""
    if session_id:
        session_id_js = f"url += `&session_id={session_id}`;"
    
    additional_css = """
.chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    border: 2px solid #00ff00;
    background: rgba(0, 255, 0, 0.05);
    padding: 15px;
    overflow: hidden;
    height: calc(100vh - 200px);
}

.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #00ff00;
}

.agent-info {
    color: #00cc00;
    font-size: 14px;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 15px;
    padding: 10px;
    background: #000000;
    border: 1px solid #00cc00;
    font-family: 'Courier New', monospace;
}

.message {
    margin: 8px 0;
    padding: 5px 0;
    word-wrap: break-word;
}

.message.user {
    color: #ffffff;
}

.message.assistant {
    color: #00ff00;
}

.message.error {
    color: #ff0000;
}

.message-time {
    color: #888888;
    font-size: 11px;
    margin-right: 8px;
}

.message-content {
    display: inline;
}

.chat-input-container {
    display: flex;
    gap: 10px;
    align-items: stretch;
}

.chat-input {
    flex: 1;
    background: #000000;
    border: 1px solid #00ff00;
    color: #ffffff;
    padding: 10px;
    font-family: inherit;
    font-size: 14px;
    resize: none;
}

.chat-input:focus {
    outline: none;
    border-color: #00cc00;
    box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
}

.send-btn {
    background: #00ff00;
    color: #000000;
    border: 2px solid #00ff00;
    padding: 10px 20px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.send-btn:hover:not(:disabled) {
    background: #000000;
    color: #00ff00;
}

.send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.streaming-indicator {
    color: #ffff00;
    font-style: italic;
    font-size: 12px;
}

.typing-indicator {
    display: inline-block;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}
    """
    
    content = f"""
        <div class="terminal-header">
            <div class="title">AI CHAT SESSION</div>
        </div>
        
        <div class="chat-container">
            <div class="chat-header">
                <div class="agent-info">
                    Agent: {agent_data['name']} | {agent_data['ai_provider'].replace('_', ' ').title()} | {agent_data['trading_chain'].title()}
                </div>
                <button class="send-btn" onclick="window.location.href='/interactive'">Back to Agents</button>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                {preloaded_messages_html}
                <div class="message assistant">
                    <span class="message-time">System:</span>
                    <span class="message-content">Connected to {agent_data['name']} ({agent_data['ai_provider']}). Type your message below and press Enter to send.</span>
                </div>
            </div>
            
            <div class="chat-input-container">
                <textarea 
                    id="chatInput" 
                    class="chat-input" 
                    placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
                    rows="3"
                ></textarea>
                <button id="sendBtn" class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <div class="instructions">
            Enter to send • Shift+Enter for new line • Escape to go back • <span class="blink">_</span>
        </div>
    """
    
    additional_js = f"""
let isStreaming = false;
let currentStreamBuffer = '';
let currentMessageElement = null;
let currentSessionId = {f"'{session_id}'" if session_id else 'null'};

// Update URL to include session_id if we have one
function updateURLWithSession(sessionId) {{
    if (sessionId) {{
        const url = new URL(window.location);
        url.searchParams.set('session_id', sessionId);
        window.history.replaceState({{}}, '', url);
        currentSessionId = sessionId;
    }}
}}

// Extract session_id from URL on page load
function extractSessionIdFromURL() {{
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('session_id') || null;
}}

function addMessage(type, content, time = null) {{
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${{type}}`;
    
    const timeStr = time || new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
    
    messageDiv.innerHTML = `
        <span class="message-time">${{timeStr}}:</span>
        <span class="message-content">${{content}}</span>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
}}

function addPreloadedMessage(type, content, time = null) {{
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${{type}}`;
    
    const timeStr = time || '';
    
    messageDiv.innerHTML = `
        <span class="message-time">${{timeStr}}</span>
        <span class="message-content">${{content}}</span>
    `;
    
    chatMessages.appendChild(messageDiv);
    return messageDiv;
}}

function updateStreamingMessage(content) {{
    if (currentMessageElement) {{
        currentMessageElement.querySelector('.message-content').textContent = content;
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }}
}}

async function sendMessage() {{
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const message = input.value.trim();
    
    if (!message || isStreaming) return;
    
    // Add user message
    addMessage('user', message);
    input.value = '';
    
    // Disable send button
    isStreaming = true;
    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending...';
    
    try {{
        // Create streaming indicator
        currentMessageElement = addMessage('assistant', '');
        updateStreamingMessage('Thinking...');
        
        // Build URL for streaming (use currentSessionId for continuity)
        let url = `/chat-stream/{agent_id}?message=${{encodeURIComponent(message)}}`;
        if (currentSessionId) {{
            url += `&session_id=${{currentSessionId}}`;
            console.log('[DEBUG] Using session_id:', currentSessionId);
        }} else {{
            console.log('[DEBUG] No session_id available, starting new session');
        }}
        console.log('[DEBUG] Opening EventSource:', url);
        
        // Create EventSource for streaming
        const eventSource = new EventSource(url);
        
        eventSource.onmessage = function(event) {{
            const data = event.data;
            
            if (data === '[DONE]') {{
                eventSource.close();
                isStreaming = false;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
                currentMessageElement = null;
            }} else if (data.startsWith('[ERROR]')) {{
                const errorMsg = data.substring(7); // Remove '[ERROR]' prefix
                updateStreamingMessage(`Error: ${{errorMsg}}`);
                eventSource.close();
                isStreaming = false;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
                currentMessageElement = null;
            }} else if (data.startsWith('[SESSION_ID:')) {{
                // Extract session ID for continuity
                const sessionId = data.substring(12); // Remove '[SESSION_ID:' prefix
                console.log('[DEBUG] Received session ID:', sessionId);
                updateURLWithSession(sessionId);
            }} else {{
                // Append streaming content
                currentStreamBuffer += data;
                updateStreamingMessage(currentStreamBuffer);
            }}
        }};
        
        eventSource.onerror = function(event) {{
            console.error('EventSource failed:', event);
            updateStreamingMessage('Connection error. Please try again.');
            eventSource.close();
            isStreaming = false;
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send';
            currentMessageElement = null;
        }};
        
        // Reset stream buffer
        currentStreamBuffer = '';
        
    }} catch (error) {{
        console.error('Error sending message:', error);
        addMessage('error', `Failed to send message: ${{error.message}}`);
        isStreaming = false;
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
        currentMessageElement = null;
    }}
}}

// Handle Enter key in textarea
document.getElementById('chatInput').addEventListener('keydown', function(e) {{
    if (e.key === 'Enter' && !e.shiftKey) {{
        e.preventDefault();
        sendMessage();
    }}
}});

// Handle Escape key
document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape' && !isStreaming) {{
        if (confirm('Are you sure you want to leave chat session?')) {{
            window.location.href = '/select-agent-for-session';
        }}
    }}
}});

// Focus input on load and initialize session ID
document.addEventListener('DOMContentLoaded', function() {{
    document.getElementById('chatInput').focus();
    
    // Extract session ID from URL if available (for resumed sessions)
    const urlSessionId = extractSessionIdFromURL();
    if (urlSessionId && !currentSessionId) {{
        currentSessionId = urlSessionId;
        console.log('[DEBUG] Loaded session ID from URL:', currentSessionId);
    }}
}});
    """
    
    return base_template(f"TradeArena Web Terminal - Chat with {agent_data['name']}", content, additional_css, additional_js)
