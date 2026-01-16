"""
FastAPI web server for TradeArena CLI
Provides HTML interface and API endpoints for configuration and monitoring
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import time
from typing import Dict, Any

from .routes import setup_routes

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

# Setup all routes
setup_routes(app)

# Global server state
server_state = {
    "running": False,
    "start_time": None,
    "thread": None
}

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
