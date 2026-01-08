#!/usr/bin/env python3
"""
TradeArena CLI - The Vibe Trading Arena for DeFi

This is the main entry point for the TradeArena CLI application.
It provides a rich, interactive interface for managing AI trading agents,
configuring strategies, monitoring performance, and managing decentralized storage.
"""

import sys
import os
import threading
import time
from pathlib import Path
from cli import MenuSystem
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Import server functionality
try:
    from server import start_server_thread, stop_server
    WEB_SERVER_AVAILABLE = True
except ImportError:
    WEB_SERVER_AVAILABLE = False

def main():
    """Main entry point for TradeArena CLI"""
    server_started = False
    try:
        # Start web server if available
        if WEB_SERVER_AVAILABLE:
            console = Console()
            console.print("[dim]Starting web interface server...[/dim]")
            success, message = start_server_thread()
            if success:
                server_started = True
                console.print(f"[bold green]✓ {message}[/bold green]")
                console.print("[dim]Web interface is now available in the background[/dim]")
            else:
                console.print(f"[bold yellow]⚠ {message}[/bold yellow]")
        
        # Initialize menu system
        menu = MenuSystem()
        
        # Display welcome message
        welcome_text = Text.from_markup(
            "[bold blue]🚀 Welcome to TradeArena CLI[/bold blue]\n\n"
            "[dim]The Vibe Trading Arena for DeFi[/dim]\n\n"
            "[dim]Starting your AI trading agent management system...[/dim]"
        )
        
        welcome_panel = Panel(
            welcome_text,
            border_style="green",
            padding=(1, 2)
        )
        
        console = Console()
        console.print(welcome_panel)
        
        # Start the main menu loop
        menu.run(server_started)
        
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[bold yellow]👋 Goodbye! Thanks for using TradeArena CLI.[/bold yellow]")
        
        # Stop web server if it was started
        if server_started and WEB_SERVER_AVAILABLE:
            stop_server()
            console.print("[dim]Web interface server stopped.[/dim]")
            
    except Exception as e:
        console = Console()
        console.print(f"\n[bold red]❌ An error occurred: {e}[/bold red]")
        console.print("[dim]Please check your configuration and try again.[/dim]")
        
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
