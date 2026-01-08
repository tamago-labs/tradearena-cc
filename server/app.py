"""
FastAPI web server for TradeArena CLI
Provides HTML interface and API endpoints for configuration and monitoring
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import time
from typing import Dict, Any

from .data import MockDataGenerator

# Initialize FastAPI app
app = FastAPI(
    title="TradeArena CLI Web Interface",
    description="Web interface for TradeArena CLI configuration and monitoring",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data generator
mock_data = MockDataGenerator()

# Global server state
server_state = {
    "running": False,
    "start_time": None,
    "thread": None
}

@app.get("/")
async def root(request: Request):
    """Main dashboard page"""
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradeArena CLI - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { 
            background: rgba(255,255,255,0.05); 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        .title { 
            font-size: 2.5em; 
            background: linear-gradient(45deg, #00ff88, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .subtitle { color: #888; font-size: 1.2em; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { 
            background: rgba(255,255,255,0.05); 
            padding: 20px; 
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,255,136,0.2); }
        .card h3 { color: #00ff88; margin-bottom: 15px; font-size: 1.3em; }
        .status { display: inline-block; padding: 5px 10px; border-radius: 20px; font-size: 0.9em; }
        .status.running { background: #00ff88; color: #000; }
        .status.stopped { background: #ff4444; color: #fff; }
        .status.paused { background: #ffaa00; color: #000; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .metric-value { font-weight: bold; color: #00d4ff; }
        .nav { 
            background: rgba(255,255,255,0.05); 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 30px;
            text-align: center;
        }
        .nav a { 
            color: #00ff88; 
            text-decoration: none; 
            margin: 0 15px; 
            padding: 10px 20px;
            border: 1px solid #00ff88;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .nav a:hover { background: #00ff88; color: #000; }
        .refresh-btn { 
            background: #00ff88; 
            color: #000; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer;
            font-weight: bold;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">TradeArena CLI</h1>
            <p class="subtitle">AI Trading Agent Management Interface</p>
        </div>

        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/settings">Settings</a>
            <a href="/agents">Agents</a>
        </div>

        <div class="grid">
            <div class="card">
                <h3>System Status</h3>
                <div class="metric">
                    <span>Server Status:</span>
                    <span class="status running">Online</span>
                </div>
                <div class="metric">
                    <span>Active Agents:</span>
                    <span class="metric-value">1 / 3</span>
                </div>
                <div class="metric">
                    <span>Chains Connected:</span>
                    <span class="metric-value">2</span>
                </div>
                <button class="refresh-btn" onclick="location.reload()">Refresh</button>
            </div>

            <div class="card">
                <h3>Performance Today</h3>
                <div class="metric">
                    <span>Daily P&L:</span>
                    <span class="metric-value" style="color: #00ff88;">+$156.75</span>
                </div>
                <div class="metric">
                    <span>Total Trades:</span>
                    <span class="metric-value">226</span>
                </div>
                <div class="metric">
                    <span>Success Rate:</span>
                    <span class="metric-value">78.8%</span>
                </div>
            </div>

            <div class="card">
                <h3>Active Agents</h3>
                <div style="margin: 15px 0;">
                    <div style="margin: 10px 0; padding: 10px; background: rgba(0,255,136,0.1); border-radius: 5px;">
                        <strong>DeFi Yield Hunter</strong>
                        <span class="status running" style="float: right;">Running</span>
                        <div style="margin-top: 5px; font-size: 0.9em; color: #888;">
                            P&L: +$1,247.50 | Trades: 47 | Success: 78.5%
                        </div>
                    </div>
                    <div style="margin: 10px 0; padding: 10px; background: rgba(255,68,68,0.1); border-radius: 5px;">
                        <strong>Arbitrage Master</strong>
                        <span class="status stopped" style="float: right;">Stopped</span>
                        <div style="margin-top: 5px; font-size: 0.9em; color: #888;">
                            P&L: +$567.25 | Trades: 23 | Success: 91.3%
                        </div>
                    </div>
                    <div style="margin: 10px 0; padding: 10px; background: rgba(255,170,0,0.1); border-radius: 5px;">
                        <strong>Market Maker Bot</strong>
                        <span class="status paused" style="float: right;">Paused</span>
                        <div style="margin-top: 5px; font-size: 0.9em; color: #888;">
                            P&L: -$234.75 | Trades: 156 | Success: 65.8%
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """)

@app.get("/settings")
async def settings():
    """Settings configuration page"""
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
    """Agents management page"""
    agents_data = mock_data.get_agents()
    
    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradeArena CLI - Agents</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #ffffff;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
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
        .agents-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
        .agent-card {{ 
            background: rgba(255,255,255,0.05); 
            padding: 25px; 
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease;
        }}
        .agent-card:hover {{ transform: translateY(-5px); }}
        .agent-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .agent-name {{ font-size: 1.3em; font-weight: bold; color: #00ff88; }}
        .agent-status {{ padding: 5px 15px; border-radius: 20px; font-size: 0.9em; }}
        .status.running {{ background: #00ff88; color: #000; }}
        .status.stopped {{ background: #ff4444; color: #fff; }}
        .status.paused {{ background: #ffaa00; color: #000; }}
        .agent-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0; }}
        .info-item {{ font-size: 0.9em; }}
        .info-label {{ color: #888; }}
        .info-value {{ color: #fff; font-weight: bold; }}
        .metrics {{ display: flex; justify-content: space-between; margin: 15px 0; }}
        .metric {{ text-align: center; }}
        .metric-value {{ font-size: 1.2em; font-weight: bold; color: #00d4ff; }}
        .metric-label {{ font-size: 0.8em; color: #888; }}
        .position {{ background: rgba(0,255,136,0.1); padding: 10px; border-radius: 5px; margin: 10px 0; }}
        .action-btn {{ 
            background: #00ff88; 
            color: #000; 
            border: none; 
            padding: 8px 16px; 
            border-radius: 5px; 
            cursor: pointer;
            margin: 5px;
            font-weight: bold;
        }}
        .danger {{ background: #ff4444; color: #fff; }}
        .warning {{ background: #ffaa00; color: #000; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">TradeArena CLI</h1>
        </div>

        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/settings">Settings</a>
            <a href="/agents">Agents</a>
        </div>

        <div class="agents-grid">
            {"".join([f'''
            <div class="agent-card">
                <div class="agent-header">
                    <span class="agent-name">{agent['name']}</span>
                    <span class="agent-status {agent['status']}">{agent['status'].upper()}</span>
                </div>
                
                <div class="agent-info">
                    <div class="info-item">
                        <span class="info-label">Type:</span>
                        <span class="info-value">{agent['type'].replace('_', ' ').title()}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Chains:</span>
                        <span class="info-value">{', '.join(agent['chains']).upper()}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Created:</span>
                        <span class="info-value">{agent['created_at'][:10]}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Last Trade:</span>
                        <span class="info-value">{agent['last_trade'][:10]}</span>
                    </div>
                </div>

                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{agent['total_trades']}</div>
                        <div class="metric-label">Total Trades</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{agent['success_rate']}%</div>
                        <div class="metric-label">Success Rate</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" style="color: {'#00ff88' if agent['total_pnl'] >= 0 else '#ff4444'}">
                            {'+' if agent['total_pnl'] >= 0 else ''}${agent['total_pnl']:,.2f}
                        </div>
                        <div class="metric-label">Total P&L</div>
                    </div>
                </div>

                {f'''<div class="position">
                    <strong>Current Position:</strong> {agent['current_position']['protocol']} - {agent['current_position']['pair']} (${agent['current_position']['value']:,.2f})
                </div>''' if agent['current_position'] else '''<div class="position"><strong>Current Position:</strong> None</div>'''}

                <div>
                    {'''<button class="action-btn warning">Pause</button>''' if agent['status'] == 'running' else ''}
                    {'''<button class="action-btn">Start</button>''' if agent['status'] == 'stopped' else ''}
                    {'''<button class="action-btn">Resume</button>''' if agent['status'] == 'paused' else ''}
                    <button class="action-btn danger">Stop</button>
                    <button class="action-btn">Configure</button>
                </div>
            </div>
            ''' for agent in agents_data])}
        </div>
    </div>
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

def run_server(host: str = "127.0.0.1", port: int = 8000):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port, log_level="info")

def start_server_thread(host: str = "127.0.0.1", port: int = 8000):
    """Start server in a background thread"""
    if server_state["running"]:
        return False, "Server is already running"
    
    def run():
        server_state["running"] = True
        server_state["start_time"] = time.time()
        uvicorn.run(app, host=host, port=port, log_level="warning")
        server_state["running"] = False
    
    server_state["thread"] = threading.Thread(target=run, daemon=True)
    server_state["thread"].start()
    
    # Give server time to start
    time.sleep(2)
    
    return True, f"Server started at http://{host}:{port}"

def stop_server():
    """Stop the server"""
    if not server_state["running"]:
        return False, "Server is not running"
    
    # Note: This is a simple implementation. In production, you might want
    # to use a more graceful shutdown mechanism
    server_state["running"] = False
    return True, "Server stopped"

if __name__ == "__main__":
    run_server()