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
    chat_session_template
)
from .agents import agent_manager, AI_PROVIDERS, TRADING_CHAINS
from .sessions import session_manager
from .tools import (
    weather_forecast
)

def create_conversation_manager() -> SlidingWindowConversationManager:
    """Create conversation manager with fixed settings for all agents"""
    return SlidingWindowConversationManager(
        window_size=15,  # Fixed window size
        should_truncate_results=True  # Fixed truncation setting
    )

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
    
    # Initialize agent based on provider
    if ai_provider == "amazon-bedrock":
        model_id = config.get('model_id', 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')
        region_name = config.get('region_name', 'us-east-1')
        
        boto_session = boto3.Session(region_name=region_name)
        model = BedrockModel(model_id=model_id, boto_session=boto_session)
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=[weather_forecast],
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state
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
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=[weather_forecast],
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state
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
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=[weather_forecast],
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state
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
        
        trading_agent = Agent(
            name=f"trading_agent_{agent_id}",
            agent_id=f"trading_agent_{agent_id}",
            tools=[weather_forecast],
            model=model,
            session_manager=session_manager,
            conversation_manager=conversation_manager,
            callback_handler=None,
            state=agent_state
        )
        
        logger.info(f"Initialized OpenAI Compatible agent: {model_id} (base_url: {base_url or 'default'})")
        return trading_agent, session_id
    
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}")

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
    
    # Include all other routes from the original file (keeping them unchanged)
    @app.get("/interactive")
    async def interactive():
        """Interactive mode page"""
        return HTMLResponse(interactive_mode_template())
    
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
        """Walrus settings page"""
        return HTMLResponse(walrus_settings_template())
    
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
