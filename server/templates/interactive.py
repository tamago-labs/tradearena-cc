"""
Interactive mode and chat session templates for TradeArena Web Terminal
"""

from ..static import SUBMENU_JS
from .base import base_template

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
                <div>
                    <button class="send-btn" onclick="window.location.href='/interactive'" style="margin-right: 10px;">Back to Agents</button>
                    <button class="send-btn" onclick="deleteSession()">Delete Session</button>
                </div>
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

// Delete session function
function deleteSession() {{
    if (confirm('Are you sure you want to delete this entire session? This action cannot be undone.')) {{
        // Use currentSessionId for deletion
        let sessionToDelete = currentSessionId;
        if (sessionToDelete) {{
            // Clean session ID by removing any trailing ] character
            sessionToDelete = sessionToDelete.replace(/\\]$/, '');
            console.log('[DEBUG] Deleting session with cleaned ID:', sessionToDelete);
            window.location.href = `/delete-session/${{sessionToDelete}}`;
        }} else {{
            alert('No session ID available for deletion.');
        }}
    }}
}}

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
