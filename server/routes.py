"""
Route handlers for TradeArena Web Terminal
All API and page routes
"""

from fastapi import Request
from fastapi.responses import HTMLResponse
from .templates import (
    main_page_template,
    interactive_mode_template,
    views_page_template,
    config_page_template,
    walrus_page_template,
    logs_page_template
)
from .data import MockDataGenerator

# Initialize data generator
mock_data = MockDataGenerator()

def setup_routes(app):
    """Setup all routes for the FastAPI app"""
    
    @app.get("/")
    async def root():
        """Main terminal interface"""
        return HTMLResponse(main_page_template())
    
    @app.get("/interactive")
    async def interactive():
        """Interactive mode page"""
        return HTMLResponse(interactive_mode_template())
    
    @app.get("/views")
    async def views():
        """Manage views page"""
        return HTMLResponse(views_page_template())
    
    @app.get("/config")
    async def config():
        """Configure agent page"""
        return HTMLResponse(config_page_template())
    
    @app.get("/walrus")
    async def walrus():
        """Walrus settings page"""
        return HTMLResponse(walrus_page_template())
    
    @app.get("/logs")
    async def logs():
        """Agent logs page"""
        return HTMLResponse(logs_page_template())
    
    @app.get("/settings")
    async def settings():
        """Settings configuration page (legacy)"""
        settings_data = mock_data.get_default_settings()
        
        return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradeArena CLI - Settings</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #ffffff;
            min-height: 100vh;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        .header {{ 
            background: rgba(255,255,255,0.05); 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        .title {{ 
            font-size: 2.5em; 
            background: linear-gradient(45deg, #00ff88, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .subtitle {{ color: #888; font-size: 1.2em; }}
        .nav {{ 
            background: rgba(255,255,255,0.05); 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 30px;
            text-align: center;
        }}
        .nav a {{ 
            color: #00ff88; 
            text-decoration: none; 
            margin: 0 15px; 
            padding: 10px 20px;
            border: 1px solid #00ff88;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}
        .nav a:hover {{ background: #00ff88; color: #000; }}
        .section {{ 
            background: rgba(255,255,255,0.05); 
            padding: 25px; 
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 20px;
        }}
        .section h2 {{ color: #00ff88; margin-bottom: 20px; font-size: 1.5em; }}
        .config-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .config-item {{ 
            background: rgba(255,255,255,0.02); 
            padding: 15px; 
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        .config-item h3 {{ color: #00d4ff; margin-bottom: 10px; }}
        .config-item p {{ margin: 5px 0; font-size: 0.9em; color: #ccc; }}
        .config-item .value {{ color: #fff; font-weight: bold; }}
        .enabled {{ color: #00ff88; }}
        .disabled {{ color: #ff4444; }}
        .toggle {{ 
            background: #333; 
            border: 1px solid #666; 
            color: #fff; 
            padding: 5px 10px; 
            border-radius: 5px; 
            cursor: pointer;
            margin-left: 10px;
        }}
        .toggle.enabled {{ background: #00ff88; color: #000; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">TradeArena CLI</h1>
            <p class="subtitle">Configuration Settings</p>
        </div>

        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/settings">Settings</a>
            <a href="/agents">Agents</a>
        </div>

        <div class="section">
            <h2>AI Providers</h2>
            <div class="config-grid">
                <div class="config-item">
                    <h3>Anthropic Claude</h3>
                    <p>Status: <span class="value enabled">Enabled</span></p>
                    <p>Model: <span class="value">{settings_data['ai_providers']['anthropic']['model']}</span></p>
                    <p>Temperature: <span class="value">{settings_data['ai_providers']['anthropic']['temperature']}</span></p>
                    <button class="toggle enabled">Enabled</button>
                </div>
                <div class="config-item">
                    <h3>OpenAI GPT</h3>
                    <p>Status: <span class="value disabled">Disabled</span></p>
                    <p>Model: <span class="value">{settings_data['ai_providers']['openai']['model']}</span></p>
                    <p>Temperature: <span class="value">{settings_data['ai_providers']['openai']['temperature']}</span></p>
                    <button class="toggle disabled">Disabled</button>
                </div>
                <div class="config-item">
                    <h3>Google Gemini</h3>
                    <p>Status: <span class="value disabled">Disabled</span></p>
                    <p>Model: <span class="value">{settings_data['ai_providers']['gemini']['model']}</span></p>
                    <p>Temperature: <span class="value">{settings_data['ai_providers']['gemini']['temperature']}</span></p>
                    <button class="toggle disabled">Disabled</button>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Trading Chains</h2>
            <div class="config-grid">
                <div class="config-item">
                    <h3>Cronos</h3>
                    <p>Status: <span class="value enabled">Enabled</span></p>
                    <p>RPC: <span class="value">https://evm-cronos.crypto.org</span></p>
                    <p>Explorer: <span class="value">cronoscan.com</span></p>
                    <button class="toggle enabled">Enabled</button>
                </div>
                <div class="config-item">
                    <h3>KAIA</h3>
                    <p>Status: <span class="value enabled">Enabled</span></p>
                    <p>RPC: <span class="value">public-en-baobab.klaytn.net</span></p>
                    <p>Explorer: <span class="value">baobab.klaytnscope.com</span></p>
                    <button class="toggle enabled">Enabled</button>
                </div>
                <div class="config-item">
                    <h3>Sui</h3>
                    <p>Status: <span class="value disabled">Disabled</span></p>
                    <p>RPC: <span class="value">fullnode.mainnet.sui.io</span></p>
                    <p>Explorer: <span class="value">suiexplorer.com</span></p>
                    <button class="toggle disabled">Disabled</button>
                </div>
                <div class="config-item">
                    <h3>Aptos</h3>
                    <p>Status: <span class="value disabled">Disabled</span></p>
                    <p>RPC: <span class="value">fullnode.mainnet.aptoslabs.com</span></p>
                    <p>Explorer: <span class="value">explorer.aptoslabs.com</span></p>
                    <button class="toggle disabled">Disabled</button>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Risk Management</h2>
            <div class="config-grid">
                <div class="config-item">
                    <h3>Trade Limits</h3>
                    <p>Max Trade Size: <span class="value">${settings_data['risk_settings']['max_trade_size_usd']:,}</span></p>
                    <p>Max Daily Trades: <span class="value">{settings_data['risk_settings']['max_daily_trades']}</span></p>
                    <p>Max Position Size: <span class="value">{settings_data['risk_settings']['max_position_size_percent']}%</span></p>
                </div>
                <div class="config-item">
                    <h3>Stop Loss / Take Profit</h3>
                    <p>Stop Loss: <span class="value">{settings_data['risk_settings']['stop_loss_percent']}%</span></p>
                    <p>Take Profit: <span class="value">{settings_data['risk_settings']['take_profit_percent']}%</span></p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Storage</h2>
            <div class="config-grid">
                <div class="config-item">
                    <h3>Walrus Storage</h3>
                    <p>Status: <span class="value enabled">Enabled</span></p>
                    <p>Endpoint: <span class="value">{settings_data['storage']['walrus']['endpoint']}</span></p>
                    <p>Publisher: <span class="value">publisher.walrus.ai</span></p>
                    <button class="toggle enabled">Enabled</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """)
    
    @app.get("/agents")
    async def agents():
        """Agents management page (legacy - redirected to main)"""
        return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Redirecting...</title></head>
<body>
<script>window.location.href = '/';</script>
</body>
</html>
        """)
    
    # API Endpoints
    @app.get("/api/settings")
    async def get_settings():
        """Get current settings"""
        return mock_data.get_default_settings()
    
    @app.get("/api/agents")
    async def get_agents():
        """Get agents list"""
        return mock_data.get_agents()
    
    @app.get("/api/status")
    async def get_status():
        """Get system status"""
        return mock_data.get_system_status()
    
    @app.get("/api/trades")
    async def get_trades(limit: int = 20):
        """Get recent trades"""
        return mock_data.get_recent_trades(limit)
    
    @app.get("/api/performance")
    async def get_performance():
        """Get performance metrics"""
        return mock_data.get_performance_metrics()