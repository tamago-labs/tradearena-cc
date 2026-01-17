"""
Agent management templates for TradeArena Web Terminal
"""

from ..static import SUBMENU_JS
from .base import base_template

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
    from ..agents import PROVIDER_CONFIGS
    
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
