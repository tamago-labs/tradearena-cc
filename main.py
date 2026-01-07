#!/usr/bin/env python3
"""
TradeArena CLI
"""

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.text import Text

from cli.config_manager import ConfigManager
from cli.setup_menu import SetupMenu
from cli.prompt_mode import PromptMode

console = Console()


def main():
    """Main entry point for the enhanced CLI tool"""
    parser = argparse.ArgumentParser(
        description="TradeArena CLI - AI Trading Competition Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py              # Run interactive mode (starts setup if needed)
  python3 main.py --setup       # Force configuration setup
  python3 main.py --config      # Show current configuration
  python3 main.py --validate    # Validate current configuration
        """
    )
    
    parser.add_argument(
        "--setup", 
        action="store_true",
        help="Run configuration setup"
    )
    parser.add_argument(
        "--config", 
        action="store_true",
        help="Show current configuration"
    )
    parser.add_argument(
        "--validate", 
        action="store_true",
        help="Validate current configuration"
    )
    parser.add_argument(
        "--version", 
        action="version",
        version="TradeArena CLI v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Handle command line arguments
    if args.setup:
        run_setup_mode(config_manager)
    elif args.config:
        show_configuration(config_manager)
    elif args.validate:
        validate_configuration(config_manager)
    else:
        run_main_mode(config_manager)


def run_setup_mode(config_manager: ConfigManager):
    """Run setup mode for configuring providers"""
    console.print("\n" + "="*60)
    console.print("🔧 TradeArena CLI Setup Mode", style="bold blue")
    console.print("="*60)
    
    setup_menu = SetupMenu(config_manager)
    
    # Keep trying setup until successful or user gives up
    while True:
        success = setup_menu.run_setup()
        if success:
            break
        else:
            if not console.input("\nPress Enter to try again or Ctrl+C to exit..."):
                break


def show_configuration(config_manager: ConfigManager):
    """Display current configuration"""
    console.print("\n" + "="*60)
    console.print("⚙️  TradeArena CLI Configuration", style="bold blue")
    console.print("="*60)
    
    if not config_manager.config_exists():
        console.print("❌ No configuration file found.", style="red")
        console.print("Run 'python3 main.py --setup' to configure.", style="yellow")
        return
    
    config = config_manager.get_config()
    
    # Display configuration in a nice format
    from cli.provider_factory import ProviderFactory
    provider_info = ProviderFactory.get_available_providers()[config.provider]
    
    console.print(f"🤖 Provider: {provider_info['name']} ({config.provider})")
    console.print(f"🧠 Model: {config.models[config.provider]}")
    console.print(f"🌡️  Temperature: {config.params.get('temperature', 0.7)}")
    console.print(f"📏 Max Tokens: {config.params.get('max_tokens', 1000)}")
    
    # Show configuration status
    configured = config.is_configured()
    status_color = "green" if configured else "red"
    status_symbol = "✅" if configured else "❌"
    console.print(f"\n{status_symbol} Status: {'Configured' if configured else 'Not Configured'}", style=status_color)
    
    if not configured:
        console.print("\n💡 To complete configuration:", style="yellow")
        if config.provider == "bedrock":
            console.print("  • Configure AWS credentials (aws configure)")
        else:
            credential_key = f"{config.provider}_api_key"
            if not config.credentials.get(credential_key):
                console.print(f"  • Set {credential_key} in configuration")


def validate_configuration(config_manager: ConfigManager):
    """Validate current configuration"""
    console.print("\n" + "="*60)
    console.print("🔍 Validating Configuration", style="bold blue")
    console.print("="*60)
    
    if not config_manager.config_exists():
        console.print("❌ No configuration file found.", style="red")
        console.print("Run 'python3 main.py --setup' to configure.", style="yellow")
        return
    
    config = config_manager.get_config()
    is_configured = config.is_configured()
    
    if is_configured:
        console.print("✅ Configuration exists and appears valid", style="green")
        console.print("💡 Note: Actual API connectivity will be tested when you first use the CLI", style="dim")
    else:
        console.print("❌ Configuration is incomplete", style="red")
        console.print("Run 'python3 main.py --setup' to complete configuration.", style="yellow")


def run_main_mode(config_manager: ConfigManager):
    """Run main CLI mode - either setup or prompt"""
    # Check if configuration exists and is valid
    config_exists = config_manager.config_exists()
    is_configured = config_manager.is_fully_configured()
    
    if not config_exists or not is_configured:
        # Show welcome and start setup
        console.print("\n" + "="*60)
        console.print("🚀 Welcome to TradeArena CLI!", style="bold blue")
        console.print("="*60)
        
        if not config_exists:
            console.print("📋 No configuration found. Let's set up your AI provider.")
        else:
            console.print("⚠️  Configuration incomplete or invalid. Let's fix that.")
        
        console.print("\nThis will help you configure access to AI models.")
        
        if Confirm.ask("\nWould you like to start setup now?", default=True):
            run_setup_mode(config_manager)
        else:
            console.print("\n💡 Run 'python3 main.py --setup' when you're ready to configure.", style="yellow")
            return
    
    # Check if configuration is minimally configured
    if not config_manager.config_exists():
        console.print("\n❌ No configuration found.", style="red")
        console.print("Please run 'python3 main.py --setup' to configure.", style="yellow")
        return
    
    # Configuration is good - start prompt mode
    try:
        prompt_mode = PromptMode(config_manager)
        prompt_mode.run()
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!", style="blue")
    except Exception as e:
        console.print(f"\n❌ Error starting prompt mode: {e}", style="red")
        console.print("Please check your configuration and try again.", style="yellow")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!", style="blue")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n❌ Fatal error: {e}", style="red")
        sys.exit(1)
