#!/usr/bin/env python3
"""
TradeArena Web Terminal - The Vibe Trading Arena for DeFi

This is the main entry point for the TradeArena Web Terminal application.
It provides a retro terminal-style web interface for managing AI trading agents,
configuring strategies, monitoring performance, and managing decentralized storage.
"""

import sys
import os
import threading
import time
from pathlib import Path

# Import server functionality
try:
    from server import start_server_thread, stop_server
    WEB_SERVER_AVAILABLE = True
except ImportError:
    WEB_SERVER_AVAILABLE = False

def main():
    """Main entry point for TradeArena Web Terminal"""
    server_started = False
    try:
        # Start web server if available
        if WEB_SERVER_AVAILABLE:
            print("Starting TradeArena Web Terminal server...")
            success, message = start_server_thread()
            if success:
                server_started = True
                print(f"✓ {message}")
                print(f"🌐 Web Terminal is now available at: {message}")
                print("📝 Open your browser and navigate to the URL above")
                print("🎮 Use arrow keys to navigate, Enter to select, Escape to go back")
                print("⏹️  Press Ctrl+C here to stop the server")
            else:
                print(f"⚠ {message}")
                sys.exit(1)
        else:
            print("❌ Web server not available. Please install required dependencies.")
            print("Run: pip install fastapi uvicorn[standard]")
            sys.exit(1)
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using TradeArena Web Terminal.")
        
        # Stop web server if it was started
        if server_started and WEB_SERVER_AVAILABLE:
            stop_server()
            print("Web Terminal server stopped.")
            
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your configuration and try again.")
        
        # Stop web server on error
        if server_started and WEB_SERVER_AVAILABLE:
            stop_server()
            
        sys.exit(1)
    finally:
        # Ensure server is stopped on exit
        if server_started and WEB_SERVER_AVAILABLE:
            stop_server()


if __name__ == "__main__":
    main()
