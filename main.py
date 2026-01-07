#!/usr/bin/env python3
"""
TradeArena CLI - The Vibe Trading Arena for DeFi

This is the main entry point for the TradeArena CLI application.
It provides a rich, interactive interface for managing AI trading agents,
configuring strategies, monitoring performance, and managing decentralized storage.
"""

import sys
import os
from pathlib import Path
from cli import MenuSystem
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

def main():
    """Main entry point for TradeArena CLI"""
    try:
        # Initialize menu system
        menu = MenuSystem()
        
        # Display welcome message
        console = Console()
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
        
        console.print(welcome_panel)
        
        # Start the main menu loop
        menu.run()
        
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[bold yellow]👋 Goodbye! Thanks for using TradeArena CLI.[/bold yellow]")
    except Exception as e:
        console = Console()
        console.print(f"\n[bold red]❌ An error occurred: {e}[/bold red]")
        console.print("[dim]Please check your configuration and try again.[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
