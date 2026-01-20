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
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models import BedrockModel
from strands.models.anthropic import AnthropicModel
from strands.models.gemini import GeminiModel
from strands.models.openai import OpenAIModel
from strands.session.file_session_manager import FileSessionManager
from .templates import (
    main_page_template,
    interactive_mode_template,
    views_page_template,
    walrus_settings_template,
    manage_agents_template,
    manage_agent_template,
    create_agent_template,
    create_agent_config_template,
    create_agent_step2_template,
    create_agent_confirm_template,
    select_agent_for_session_template,
    chat_session_template,
    settings_template
)
from .settings import settings_manager
from .agents import agent_manager, AI_PROVIDERS, TRADING_CHAINS
from .sessions import session_manager
from .tools import ( 
    create_custom_view,
    list_available_views
)
from .views_manager import views_manager
from .mcp_manager import mcp_manager

def create_conversation_manager() -> SlidingWindowConversationManager:
    """Create conversation manager with fixed settings for all agents"""
    return SlidingWindowConversationManager(
        window_size=15,  # Fixed window size
        should_truncate_results=True  # Fixed truncation setting
    )

def get_tradearena_system_prompt() -> str:
    """Get the TradeArena System Prompt with conditional Walrus persistence and Web Search"""
    
    # Check if Walrus and Web Search are enabled
    walrus_enabled = settings_manager.is_walrus_enabled()
    web_search_enabled = settings_manager.is_web_search_enabled()
    
    # Part 1: Role & Views (always included)
    system_prompt = """You are TradeArena Agent, a specialized AI agent for cryptocurrency trading across Cronos, Kaia, and Sui networks.

Core Responsibilities:
- Execute trades (swaps, lending, borrowing, staking)
- Analyze market data and risks
- Optimize protocol selection
- Manage portfolios effectively

Required Trading Sequence:
1. Market analysis using available data sources
2. Risk assessment and position sizing
3. Protocol and route optimization
4. Trade execution with verification
5. Performance documentation

Always provide reasoning and use markdown for clear communication."""

    # Part 2: Walrus Persistence (conditional)
    if walrus_enabled:
        system_prompt += """

## Walrus Collective Intelligence

Store all trading activities on Walrus for shared learning:
- Store trade decisions before execution using `trade_arena_walrus_store`
- Store results after completion using `trade_arena_walrus_store`
- Store market analysis insights using `trade_arena_walrus_store`

This enables collective intelligence sharing across all TradeArena agents."""

    # Part 3: Web Search Capability (conditional)
    if web_search_enabled:
        system_prompt += """

## Internet Search Capability

You can search the internet for real-time information using `http_request`:
- Get latest market news and price updates
- Research project fundamentals and announcements
- Verify market sentiment and social media trends
- Access real-time trading data from external sources

Use web search when you need current information that may not be available through blockchain data alone."""

    return system_prompt

def initialize_strands_agent(agent_data: dict, agent_id: str, session_id: str = None) -> tuple[Agent, str]:
    """Initialize a Strands agent with the given configuration"""

    # Extract configuration from agent data
    ai_provider = agent_data.get('ai_provider', 'anthropic')
    config = agent_data.get('config', {})
    
    # Get the conditional TradeArena System Prompt
    system_prompt = get_tradearena_system_prompt()
    
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
    
    # Create conversation manager with fixed settings
    conversation_manager = create_conversation_manager()
    
    # Create sanitized agent state (no sensitive data in session state)
    sanitized_config = {}
    sensitive_fields = ['api_key', 'region_name', 'base_url']
    for key, value in config.items():
        if key not in sensitive_fields:
            sanitized_config[key] = value
    
    agent_state = {
        "agent_config": {
            "id": agent_id,
            "name": agent_data.get('name', 'Unknown Agent'),
            "ai_provider": ai_provider,
            "trading_chain": agent_data.get('trading_chain', 'unknown'),
            "config": sanitized_config
        }
    }
    
    # Get trading chain for MCP tool selection
    trading_chain = agent_data.get('trading_chain', 'unknown')
    
    # Check if web search is enabled to add http_request tool
    web_search_enabled = settings_manager.is_web_search_enabled()
    
    # Import http_request tool only if web search is enabled
    additional_tools = [create_custom_view, list_available_views]
    if web_search_enabled:
        try:
            from strands_tools import http_request
            additional_tools.append(http_request)
            logger.info("Web search enabled - added http_request tool")
        except ImportError:
            logger.warning("strands_tools not available - web search disabled")
    
    # Initialize agent based on provider
    if ai_provider == "amazon-bedrock":
        model_id = config.get('model_id', 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')
        region_name = config.get('region_name', 'us-east-1')
        
        boto_session = boto3.Session(region_name=region_name)
        model = BedrockModel(model_id=model_id, boto_session=boto_session)
        
        # Get MCP tools for this trading chain with persistent clients
        mcp_tools, persistent_clients = mcp_manager.get_mcp_tools(trading_chain)
        all_tools = mcp_tools + additional_tools
        
        # Store persistent clients separately (not in agent state to avoid JSON serialization issues)
        # We'll manage them through the MCP manager instead
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=all_tools,
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state,
            system_prompt=system_prompt
        )
        
        logger.info(f"Initialized Amazon Bedrock agent: {model_id} in {region_name}")
        return trading_agent, session_id
    
    elif ai_provider == "anthropic":
        api_key = config.get('api_key')
        if not api_key:
            raise ValueError("API key is required for Anthropic provider")
        
        model_id = config.get('model_id', 'claude-sonnet-4-5-20250929')
        max_tokens = config.get('max_tokens', 4096)
        
        model = AnthropicModel(
            client_args={"api_key": api_key},
            model_id=model_id,
            max_tokens=max_tokens
        )
        
        # Get MCP tools for this trading chain with persistent clients
        mcp_tools, persistent_clients = mcp_manager.get_mcp_tools(trading_chain)
        all_tools = mcp_tools + additional_tools
        
        # Store persistent clients separately (not in agent state to avoid JSON serialization issues)
        # We'll manage them through the MCP manager instead
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=all_tools,
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state,
            system_prompt=system_prompt
        )
        
        logger.info(f"Initialized Anthropic agent: {model_id}")
        return trading_agent, session_id
    
    elif ai_provider == "gemini":
        api_key = config.get('api_key')
        if not api_key:
            raise ValueError("API key is required for Gemini provider")
        
        model_id = config.get('model_id', 'gemini-2.5-flash')
        max_output_tokens = config.get('max_output_tokens', 2048)
        temperature = config.get('temperature', 0.7)
        top_p = config.get('top_p', 0.9)
        top_k = config.get('top_k', 40)
        
        model = GeminiModel(
            client_args={"api_key": api_key},
            model_id=model_id,
            params={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
                "top_p": top_p,
                "top_k": top_k
            }
        )
        
        # Get MCP tools for this trading chain with persistent clients
        mcp_tools, persistent_clients = mcp_manager.get_mcp_tools(trading_chain)
        all_tools = mcp_tools + additional_tools
        
        # Store persistent clients separately (not in agent state to avoid JSON serialization issues)
        # We'll manage them through the MCP manager instead
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=all_tools,
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state,
            system_prompt=system_prompt
        )
        
        logger.info(f"Initialized Gemini agent: {model_id}")
        return trading_agent, session_id
    
    elif ai_provider == "openai-compatible":
        api_key = config.get('api_key')
        if not api_key:
            raise ValueError("API key is required for OpenAI Compatible provider")
        
        model_id = config.get('model_id', 'gpt-4o')
        base_url = config.get('base_url')
        max_tokens = config.get('max_tokens', 4000)
        temperature = config.get('temperature', 0.7)
        
        client_args = {"api_key": api_key}
        if base_url:
            client_args["base_url"] = base_url
        
        model = OpenAIModel(
            client_args=client_args,
            model_id=model_id,
            params={
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        
        # Get MCP tools for this trading chain with persistent clients
        mcp_tools, persistent_clients = mcp_manager.get_mcp_tools(trading_chain)
        all_tools = mcp_tools + additional_tools
        
        # Store persistent clients separately (not in agent state to avoid JSON serialization issues)
        # We'll manage them through the MCP manager instead
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=all_tools,
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state,
            system_prompt=system_prompt
        )
        
        logger.info(f"Initialized OpenAI Compatible agent: {model_id} (base_url: {base_url or 'default'})")
        return trading_agent, session_id
    
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}")

def cleanup_agent_resources(agent_instance: Agent):
    """Clean up resources associated with an agent"""
    try:
        # Get trading chain from agent state to clean up MCP clients
        agent_state = getattr(agent_instance, 'state', {})
        trading_chain = agent_state.get("agent_config", {}).get("trading_chain", "unknown")
        
        # Clean up MCP clients through the MCP manager
        if trading_chain and trading_chain != "unknown":
            logger.info(f"Cleaning up MCP clients for trading chain: {trading_chain}")
            mcp_manager.close_clients(trading_chain)
            
    except Exception as e:
        logger.error(f"Error during agent cleanup: {e}")

def get_agent_data_for_session(agent_id: str, session_id: str = None) -> dict:
    """
    Get agent data for a session, combining session state with agent manager data
    This function ensures we have complete agent configuration (including sensitive data)
    while maintaining security by only storing non-sensitive data in session state
    """
    print(f"[DEBUG] Getting agent data for agent_id: {agent_id}, session_id: {session_id}")
    
    # If we have a session_id, try to get agent config from session state first
    if session_id:
        session_agent_config = session_manager.get_agent_config_for_resume(session_id)
        if session_agent_config:
            print(f"[DEBUG] Found agent config in session state: {session_agent_config}")
            
            # Use the config_agent_id from session state for getting full agent config
            config_agent_id = session_agent_config.get("id", agent_id)
            print(f"[DEBUG] Using config_agent_id: {config_agent_id}")
            
            # Get full agent config from agent manager (includes sensitive data)
            full_agent_config = agent_manager.get_agent(config_agent_id)
            if full_agent_config:
                print(f"[DEBUG] Found full agent config in agent manager: {full_agent_config.get('name', 'Unknown')}")
                
                # Combine session state (non-sensitive) with agent manager (full config)
                merged_agent_data = {
                    "id": session_agent_config.get("id", config_agent_id),
                    "name": session_agent_config.get("name", full_agent_config.get("name", "Unknown Agent")),
                    "ai_provider": session_agent_config.get("ai_provider", full_agent_config.get("ai_provider", "anthropic")),
                    "trading_chain": session_agent_config.get("trading_chain", full_agent_config.get("trading_chain", "unknown")),
                    "config": full_agent_config.get("config", {})  # Use full config with sensitive data
                }
                print(f"[DEBUG] Successfully merged agent data")
                return merged_agent_data
            else:
                print(f"[DEBUG] Agent not found in agent manager, using session config only")
                return session_agent_config
        else:
            print(f"[DEBUG] No agent config found in session state")
    
    # Fallback to agent manager only
    print(f"[DEBUG] Using agent manager fallback")
    agent_data = agent_manager.get_agent(agent_id)
    if agent_data:
        print(f"[DEBUG] Found agent in agent manager: {agent_data.get('name', 'Unknown')}")
    else:
        print(f"[DEBUG] Agent not found in agent manager either")
    
    return agent_data

def setup_routes(app):
    """Setup all routes for the FastAPI app"""
    
    @app.get("/")
    async def root():
        """Main terminal interface"""
        return HTMLResponse(main_page_template(agent_manager.get_agents()))
    
    @app.get("/select-agent-for-session")
    async def select_agent_for_session():
        """Select agent for session page"""
        return HTMLResponse(select_agent_for_session_template(agent_manager.get_agents()))
    
    @app.get("/chat-session/{agent_id}")
    async def chat_session(agent_id: str, session_id: str = Query(None)):
        """Chat session page for specific agent"""
        agent_data = agent_manager.get_agent(agent_id)
        if agent_data:
            # Load preloaded messages if session_id provided
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
        # Clean session_id
        if session_id:
            session_id = session_id.rstrip(']').strip()
        
        print(f"[DEBUG] Chat stream requested for agent: {agent_id}, message: {message}, session_id: {session_id}")
        
        # Get agent data using our clean function
        agent_data = get_agent_data_for_session(agent_id, session_id)
        
        if not agent_data:
            print(f"[DEBUG] Agent not found: {agent_id}")
            return {"error": "Agent not found"}
        
        print(f"[DEBUG] Agent data retrieved successfully: {agent_data.get('name', 'Unknown')}")
        
        agent_instance = None
        try:
            # Initialize agent with configuration
            print(f"[DEBUG] Initializing Strands agent...")
            agent_instance, agent_session_id = initialize_strands_agent(agent_data, agent_id, session_id)
            print(f"[DEBUG] Agent initialized successfully with session ID: {agent_session_id}")
            
            async def generate_response():
                try:
                    print(f"[DEBUG] Starting stream for message: {message}")
                    
                    # Send session info as first message
                    if agent_session_id:
                        yield f"data: [SESSION_ID:{agent_session_id}]\n\n"
                        print(f"[DEBUG] Sent session ID to frontend: {agent_session_id}")
                    
                    text_sent = False
                    
                    # Stream response from agent
                    agent_stream = agent_instance.stream_async(message)
                    async for event in agent_stream:
                        print(f"[DEBUG] Stream event type: {type(event)}, content: {event}")
                        
                        # Extract text content with priority order
                        text_content = ""
                        if isinstance(event, dict):
                            if 'data' in event and isinstance(event['data'], str) and event['data'].strip():
                                text_content = event['data']
                                print(f"[DEBUG] Processing data field: '{text_content}'")
                                text_sent = True
                            elif 'message' in event and not text_sent:
                                message_data = event['message']
                                if isinstance(message_data, dict) and 'content' in message_data:
                                    content_list = message_data['content']
                                    if content_list and len(content_list) > 0:
                                        first_content = content_list[0]
                                        if isinstance(first_content, dict) and 'text' in first_content:
                                            text_content = first_content['text']
                                            print(f"[DEBUG] Processing message field: '{text_content}'")
                            elif 'event' in event:
                                event_data = event['event']
                                if isinstance(event_data, dict) and 'contentBlockDelta' in event_data:
                                    print(f"[DEBUG] Skipping contentBlockDelta to prevent duplication")
                                    continue
                        elif isinstance(event, str):
                            text_content = event
                        
                        # Send non-empty text content
                        if text_content and text_content.strip():
                            yield f"data: {text_content}\n\n"
                    
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    print(f"[DEBUG] Stream error: {str(e)}")
                    import traceback
                    print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                    yield f"data: [ERROR] {str(e)}\n\n"
                finally:
                    # Clean up agent resources when stream ends
                    if agent_instance:
                        cleanup_agent_resources(agent_instance)
            
            return StreamingResponse(
                generate_response(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        except Exception as e:
            print(f"[DEBUG] Agent initialization error: {str(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            
            # Clean up on error
            if agent_instance:
                cleanup_agent_resources(agent_instance)
                
            return {"error": str(e)}
    
    @app.get("/resume-session/{session_id}")
    async def resume_session(session_id: str):
        """Resume a specific session - Simplified Version"""
        try:
            print(f"[DEBUG] Resuming session: {session_id}")
            
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
            
            # Get session info
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
            print(f"[DEBUG] Full agent_id from session: {agent_id_full}")
            
            # Extract base agent_id (remove "trading_agent_" prefix if present)
            if agent_id_full.startswith("trading_agent_"):
                base_agent_id = agent_id_full.replace("trading_agent_", "")
                print(f"[DEBUG] Extracted base agent_id: {base_agent_id}")
            else:
                base_agent_id = agent_id_full
                print(f"[DEBUG] Using agent_id as is: {base_agent_id}")
            
            if not base_agent_id:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Agent Not Found</title></head>
<body>
<script>alert('Agent not found for this session'); window.location.href='/select-agent-for-session';</script>
</body>
</html>
                """)
            
            # Get agent data using our clean function
            agent_data = get_agent_data_for_session(base_agent_id, session_id)
            
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
            
            print(f"[DEBUG] Successfully got agent data for resume: {agent_data.get('name', 'Unknown')}")
            
            # Return chat session with preloaded messages
            return HTMLResponse(chat_session_template(base_agent_id, agent_data, session_id, messages))
            
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
        """Resume most recent session"""
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
    
    # Include all other routes from the original file (keeping them unchanged)
    @app.get("/interactive")
    async def interactive():
        """Interactive mode page"""
        return HTMLResponse(interactive_mode_template())
    
    @app.get("/views")
    async def views():
        """Manage views page"""
        return HTMLResponse(views_page_template())
    
    @app.get("/views/{filename}")
    async def serve_view(filename: str):
        """Serve individual view HTML file"""
        try:
            # Security check - only allow .html files
            if not filename.endswith('.html'):
                return HTMLResponse("Access denied", status_code=403)
            
            # Get view content
            content = views_manager.get_view_content(filename)
            if content is None:
                return HTMLResponse("View not found", status_code=404)
            
            return HTMLResponse(content)
        except Exception as e:
            print(f"[DEBUG] Error serving view {filename}: {e}")
            return HTMLResponse("Error loading view", status_code=500)
    
    @app.get("/api/views")
    async def get_views():
        """Get all views API endpoint"""
        try:
            views = views_manager.get_all_views()
            return {"views": views}
        except Exception as e:
            print(f"[DEBUG] Error getting views: {e}")
            return {"views": [], "error": str(e)}
    
    @app.delete("/api/views/{filename}")
    async def delete_view_api(filename: str):
        """Delete a specific view API endpoint"""
        try:
            # Security check - only allow .html files
            if not filename.endswith('.html'):
                return {"error": "Invalid file type"}
            
            success = views_manager.delete_view(filename)
            if success:
                return {"success": True, "message": "View deleted successfully"}
            else:
                return {"error": "View not found"}
        except Exception as e:
            print(f"[DEBUG] Error deleting view {filename}: {e}")
            return {"error": str(e)}
    
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
        config_params = dict(request.query_params)
        config_params.pop('provider', None)
        return HTMLResponse(create_agent_step2_template(provider, config_params))
    
    @app.get("/create-agent/confirm")
    async def create_agent_confirm(request: Request, provider: str = Query(...), chain: str = Query(...)):
        """Create agent confirmation page"""
        config_params = dict(request.query_params)
        config_params.pop('provider', None)
        config_params.pop('chain', None)
        return HTMLResponse(create_agent_confirm_template(provider, chain, config_params))
    
    @app.get("/create-agent/final")
    async def create_agent_final(request: Request, provider: str = Query(...), chain: str = Query(...)):
        """Finalize agent creation"""
        try:
            config_params = dict(request.query_params)
            config_params.pop('provider', None)
            config_params.pop('chain', None)
            config = {k: v for k, v in config_params.items() if v and v != ""}
            
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
        """Walrus settings page (legacy - redirected to settings)"""
        return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Redirecting...</title></head>
<body>
<script>window.location.href = '/settings';</script>
</body>
</html>
        """)
    
    @app.get("/settings")
    async def settings():
        """Settings page with Walrus configuration"""
        try:
            config = settings_manager.load_settings()
            return HTMLResponse(settings_template(config))
        except Exception as e:
            print(f"[DEBUG] Error loading settings: {e}")
            # Return settings page with default config on error
            return HTMLResponse(settings_template())
    
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
    
    @app.get("/delete-session/{session_id}")
    async def delete_session(session_id: str):
        """Delete a specific session and redirect to interactive mode"""
        try:
            # Clean session ID by removing any trailing ] character
            cleaned_session_id = session_id.rstrip(']')
            print(f"[DEBUG] Deleting session: {session_id} -> cleaned: {cleaned_session_id}")
            success = session_manager.delete_session(cleaned_session_id)
            
            if success:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Session Deleted</title></head>
<body>
<script>alert('Session deleted successfully!'); window.location.href='/interactive';</script>
</body>
</html>
                """)
            else:
                return HTMLResponse("""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Session not found or could not be deleted'); window.location.href='/interactive';</script>
</body>
</html>
                """)
        except Exception as e:
            print(f"[DEBUG] Error deleting session: {e}")
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<script>alert('Error deleting session: {str(e)}'); window.location.href='/interactive';</script>
</body>
</html>
            """)
    
    # Settings API Endpoints
    @app.post("/api/settings/save")
    async def save_settings(request: Request):
        """Save settings API endpoint"""
        try:
            settings_data = await request.json()
            success = settings_manager.save_settings(settings_data)
            
            if success:
                return {"success": True, "message": "Settings saved successfully"}
            else:
                return {"success": False, "error": "Failed to save settings"}
        except Exception as e:
            print(f"[DEBUG] Error saving settings: {e}")
            return {"success": False, "error": str(e)}
    
    @app.get("/api/settings/load")
    async def load_settings():
        """Load settings API endpoint"""
        try:
            settings = settings_manager.load_settings()
            return {"success": True, "settings": settings}
        except Exception as e:
            print(f"[DEBUG] Error loading settings: {e}")
            return {"success": False, "error": str(e)}
