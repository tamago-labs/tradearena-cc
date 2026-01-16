"""
Route handlers for TradeArena
All API and page routes
"""

from fastapi import Request, Query
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
import asyncio
import uuid
import os
import logging
import boto3
from strands import Agent
from strands.models import BedrockModel
from strands.session.file_session_manager import FileSessionManager
from .templates import (
    main_page_template,
    interactive_mode_template,
    views_page_template,
    walrus_page_template,
    logs_page_template,
    manage_agents_template,
    manage_agent_template,
    create_agent_template,
    create_agent_config_template,
    create_agent_step2_template,
    create_agent_confirm_template,
    select_agent_for_session_template,
    chat_session_template
)
from .data import MockDataGenerator
from .agents import agent_manager, AI_PROVIDERS, TRADING_CHAINS
from .sessions import session_manager

# Initialize data generator
mock_data = MockDataGenerator()

def initialize_strands_agent(agent_data: dict, agent_id: str, session_id: str = None) -> tuple[Agent, str]:
    """Initialize a Strands agent with the given configuration"""
    
    # Extract configuration from agent data
    ai_provider = agent_data.get('ai_provider', 'anthropic')
    config = agent_data.get('config', {})
    
    # Setup logging for this specific agent
    logger = logging.getLogger(f"strands.{agent_id}")
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Use existing session ID if provided, otherwise create new one
    if session_id is None:
        session_id = str(uuid.uuid4())
        logger.info(f"Creating new session: {session_id}")
    else:
        logger.info(f"Using existing session: {session_id}")
    
    sessions_dir = os.path.join(os.getcwd(), "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=sessions_dir
    )
    
    # Initialize agent based on provider
    if ai_provider == "amazon-bedrock":
        model_id = config.get('model_id', 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')
        region_name = config.get('region_name', 'us-east-1')
        
        # Create boto3 session
        boto_session = boto3.Session(region_name=region_name)
        
        # Initialize Bedrock model
        model = BedrockModel(
            model_id=model_id,
            boto_session=boto_session
        )
        
        # Create agent without tools as specified
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=[],  # No tools as requested
            model=model,
            session_manager=session_manager,
            callback_handler=None  # No callback handler for streaming
        )
        
        logger.info(f"Initialized Amazon Bedrock agent: {model_id} in {region_name}")
        return trading_agent, session_id
    
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}. Only Amazon Bedrock is supported for now.")

def setup_routes(app):
    """Setup all routes for the FastAPI app"""
    
    @app.get("/")
    async def root():
        """Main terminal interface"""
        return HTMLResponse(main_page_template(agent_manager.get_agents()))
    
    @app.get("/interactive")
    async def interactive():
        """Interactive mode page"""
        return HTMLResponse(interactive_mode_template())
    
    @app.get("/select-agent-for-session")
    async def select_agent_for_session():
        """Select agent for session page"""
        return HTMLResponse(select_agent_for_session_template(agent_manager.get_agents()))
    
    @app.get("/chat-session/{agent_id}")
    async def chat_session(agent_id: str, session_id: str = Query(None)):
        """Chat session page for specific agent"""
        agent_data = agent_manager.get_agent(agent_id)
        if agent_data:
            # If session_id is provided, load preloaded messages for continuity
            messages = []
            if session_id:
                try:
                    messages = session_manager.get_session_messages(session_id)
                except Exception as e:
                    print(f"[DEBUG] Error loading session messages: {e}")
                    messages = []
            
            return HTMLResponse(chat_session_template(agent_id, agent_data, session_id, messages))
        else:
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Agent Not Found</title></head>
<body>
<script>alert('Agent not found'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
    
    @app.get("/chat-stream/{agent_id}")
    async def chat_stream(agent_id: str, message: str = Query(...), session_id: str = Query(None)):
        """Streaming endpoint for chat messages"""
        # Clean session_id by removing any trailing brackets or whitespace
        if session_id:
            session_id = session_id.rstrip(']').strip()
        print(f"[DEBUG] Chat stream requested for agent: {agent_id}, message: {message}, session_id: {session_id}")
        
        agent_data = agent_manager.get_agent(agent_id)
        if not agent_data:
            print(f"[DEBUG] Agent not found: {agent_id}")
            return {"error": "Agent not found"}
        
        print(f"[DEBUG] Agent data: {agent_data}")
        
        try:
            # Initialize agent with configuration (pass session_id if provided for continuity)
            print(f"[DEBUG] Initializing Strands agent...")
            agent_instance, agent_session_id = initialize_strands_agent(agent_data, agent_id, session_id)
            print(f"[DEBUG] Agent initialized successfully with session ID: {agent_session_id}")
            
            async def generate_response():
                try:
                    print(f"[DEBUG] Starting stream for message: {message}")
                    
                    # Send session info as first message if available
                    if agent_session_id:
                        yield f"data: [SESSION_ID:{agent_session_id}]\n\n"
                        print(f"[DEBUG] Sent session ID to frontend: {agent_session_id}")
                    
                    # Track if we've already sent text content to avoid duplication
                    text_sent = False
                    
                    # Stream response from agent
                    agent_stream = agent_instance.stream_async(message)
                    async for event in agent_stream:
                        print(f"[DEBUG] Stream event type: {type(event)}, content: {event}")
                        
                        # Extract text content from different event types
                        text_content = ""
                        if isinstance(event, dict):
                            # Handle dictionary events - STRICT PRIORITY to avoid duplication
                            if 'data' in event and isinstance(event['data'], str) and event['data'].strip():
                                # This is the primary text content - most reliable
                                text_content = event['data']
                                print(f"[DEBUG] Processing data field: '{text_content}'")
                                text_sent = True  # Mark that we've sent text
                            elif 'message' in event:
                                # Handle complete message events - ONLY if no data field was sent
                                if not text_sent:
                                    message_data = event['message']
                                    if isinstance(message_data, dict) and 'content' in message_data:
                                        content_list = message_data['content']
                                        if content_list and len(content_list) > 0:
                                            # Extract text from first content item
                                            first_content = content_list[0]
                                            if isinstance(first_content, dict) and 'text' in first_content:
                                                text_content = first_content['text']
                                                print(f"[DEBUG] Processing message field (fallback): '{text_content}'")
                                else:
                                    print(f"[DEBUG] Skipping message field - text already sent via data field")
                            elif 'event' in event:
                                event_data = event['event']
                                if isinstance(event_data, dict):
                                    if 'contentBlockDelta' in event_data:
                                        # IMPORTANT: Skip contentBlockDelta entirely to avoid duplication
                                        # The data field above already contains the same text
                                        print(f"[DEBUG] Skipping contentBlockDelta to prevent duplication")
                                        continue
                                    elif 'messageStart' in event_data or 'messageStop' in event_data or 'contentBlockStop' in event_data:
                                        # Control events, skip content
                                        print(f"[DEBUG] Skipping control event: {event_data}")
                                        continue
                                    elif 'metadata' in event_data:
                                        # Metadata events, skip content
                                        print(f"[DEBUG] Skipping metadata event")
                                        continue
                        elif isinstance(event, str):
                            # Handle string events directly
                            text_content = event
                        
                        # Only send non-empty text content
                        if text_content and text_content.strip():
                            yield f"data: {text_content}\n\n"
                    
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    print(f"[DEBUG] Stream error: {str(e)}")
                    import traceback
                    print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                    yield f"data: [ERROR] {str(e)}\n\n"
            
            return StreamingResponse(
                generate_response(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        except Exception as e:
            print(f"[DEBUG] Agent initialization error: {str(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return {"error": str(e)}
    
    @app.get("/views")
    async def views():
        """Manage views page"""
        return HTMLResponse(views_page_template())
    
    @app.get("/manage-agents")
    async def manage_agents():
        """Manage agents page"""
        return HTMLResponse(manage_agents_template(agent_manager.get_agents()))
    
    @app.get("/manage-agent/{agent_id}")
    async def manage_agent(agent_id: str):
        """Manage individual agent page"""
        agent_data = agent_manager.get_agent(agent_id)
        if agent_data:
            return HTMLResponse(manage_agent_template(agent_id, agent_data))
        else:
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Agent Not Found</title></head>
<body>
<script>alert('Agent not found'); window.location.href='/manage-agents';</script>
</body>
</html>
            """)
    
    @app.get("/create-agent")
    async def create_agent():
        """Create new agent page"""
        return HTMLResponse(create_agent_template())
    
    @app.get("/create-agent/config")
    async def create_agent_config(provider: str = Query(...)):
        """Create agent configuration step - provider-specific configuration"""
        return HTMLResponse(create_agent_config_template(provider))
    
    @app.get("/create-agent/step2")
    async def create_agent_step2(request: Request, provider: str = Query(...)):
        """Create agent step 2 - select trading chain"""
        # Extract all query parameters except 'provider' as config params
        config_params = dict(request.query_params)
        config_params.pop('provider', None)  # Remove provider from config params
        return HTMLResponse(create_agent_step2_template(provider, config_params))
    
    @app.get("/create-agent/confirm")
    async def create_agent_confirm(request: Request, provider: str = Query(...), chain: str = Query(...)):
        """Create agent confirmation page"""
        # Extract all query parameters except 'provider' and 'chain' as config params
        config_params = dict(request.query_params)
        config_params.pop('provider', None)  # Remove provider from config params
        config_params.pop('chain', None)     # Remove chain from config params
        return HTMLResponse(create_agent_confirm_template(provider, chain, config_params))
    
    @app.get("/create-agent/final")
    async def create_agent_final(request: Request, provider: str = Query(...), chain: str = Query(...)):
        """Finalize agent creation"""
        try:
            # Extract all query parameters except 'provider' and 'chain' as config params
            config_params = dict(request.query_params)
            config_params.pop('provider', None)  # Remove provider from config params
            config_params.pop('chain', None)     # Remove chain from config params
            
            # Filter out empty config values and create config dict
            config = {k: v for k, v in config_params.items() if v and v != ""}
            
            # Create the agent with UUID-based ID and descriptive name
            new_agent = agent_manager.create_agent(
                ai_provider=provider,
                trading_chain=chain,
                config=config if config else None
            )
            
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head><title>Agent Created</title></head>
<body>
<script>alert('Agent {new_agent['name']} created successfully!\\nID: {new_agent['id']}'); window.location.href='/manage-agents';</script>
</body>
</html>
            """)
        except Exception as e:
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Error creating agent: {str(e)}'); window.location.href='/manage-agents';</script>
</body>
</html>
            """)
    
    @app.get("/delete-agent/{agent_id}")
    async def delete_agent(agent_id: str):
        """Delete agent"""
        try:
            success = agent_manager.delete_agent(agent_id)
            if success:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Agent Deleted</title></head>
<body>
<script>alert('Agent deleted successfully!'); window.location.href='/manage-agents';</script>
</body>
</html>
                """)
            else:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Agent not found'); window.location.href='/manage-agents';</script>
</body>
</html>
                """)
        except Exception as e:
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Error deleting agent: {str(e)}'); window.location.href='/manage-agents';</script>
</body>
</html>
            """)
    
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
            <a href="/manage-agents">Agents</a>
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
        """Agents management page (legacy - redirected to manage agents)"""
        return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Redirecting...</title></head>
<body>
<script>window.location.href = '/manage-agents';</script>
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
        return {"agents": agent_manager.get_agents()}
    
    @app.get("/api/ai-providers")
    async def get_ai_providers():
        """Get available AI providers"""
        return {"providers": AI_PROVIDERS}
    
    @app.get("/api/trading-chains")
    async def get_trading_chains():
        """Get available trading chains"""
        return {"chains": TRADING_CHAINS}
    
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
    
    # Session Management Routes
    @app.get("/api/sessions")
    async def get_sessions():
        """Get all available sessions"""
        try:
            sessions = session_manager.list_sessions()
            return {"sessions": sessions}
        except Exception as e:
            print(f"[DEBUG] Error getting sessions: {e}")
            return {"sessions": [], "error": str(e)}
    
    @app.get("/api/sessions/{session_id}/messages")
    async def get_session_messages(session_id: str):
        """Get messages from a specific session"""
        try:
            messages = session_manager.get_session_messages(session_id)
            return {"messages": messages}
        except Exception as e:
            print(f"[DEBUG] Error getting session messages: {e}")
            return {"messages": [], "error": str(e)}
    
    @app.get("/api/sessions/latest")
    async def get_latest_session():
        """Get the most recent session"""
        try:
            session = session_manager.get_latest_session()
            return {"session": session}
        except Exception as e:
            print(f"[DEBUG] Error getting latest session: {e}")
            return {"session": None, "error": str(e)}
    
    @app.get("/resume-session/{session_id}")
    async def resume_session(session_id: str):
        """Resume a specific session"""
        try:
            # Get session messages
            messages = session_manager.get_session_messages(session_id)
            if not messages:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Session Not Found</title></head>
<body>
<script>alert('Session not found or has no messages'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
            
            # Extract agent info from the first message or session
            session_list = session_manager.list_sessions()
            session_info = None
            for s in session_list:
                if s.get("session_id") == session_id:
                    session_info = s
                    break
            
            if not session_info:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Session Not Found</title></head>
<body>
<script>alert('Session not found'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
            
            # Extract agent_id from session info
            agent_id_full = session_info.get("agent_info", {}).get("agent_id", "")
            # Extract the short agent_id from the full agent_id (remove "trading_agent_" prefix)
            agent_id = agent_id_full.replace("trading_agent_", "") if agent_id_full.startswith("trading_agent_") else agent_id_full
            
            if not agent_id:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Agent Not Found</title></head>
<body>
<script>alert('Agent not found for this session'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
            
            # Get agent data
            agent_data = agent_manager.get_agent(agent_id)
            if not agent_data:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Agent Not Found</title></head>
<body>
<script>alert('Agent not found'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
            
            # Return chat session with preloaded messages (pass session_id for continuity)
            return HTMLResponse(chat_session_template(agent_id, agent_data, session_id, messages))
        except Exception as e:
            print(f"[DEBUG] Error resuming session: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Error resuming session: {str(e)}'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
            """)
    
    @app.get("/resume-latest")
    async def resume_latest_session():
        """Resume the most recent session"""
        try:
            latest_session = session_manager.get_latest_session()
            if not latest_session:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>No Sessions</title></head>
<body>
<script>alert('No previous sessions found'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
            
            session_id = latest_session.get("session_id")
            return await resume_session(session_id)
        except Exception as e:
            print(f"[DEBUG] Error resuming latest session: {e}")
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Error resuming latest session'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
            """)
