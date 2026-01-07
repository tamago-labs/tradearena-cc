"""Prompt mode interface - Claude Code/Cline-like interactive experience"""
import sys
import readline
from typing import List, Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table

from cli.config_manager import ConfigManager
from cli.provider_factory import ProviderFactory

console = Console()


class PromptMode:
    """Interactive prompt mode like Claude Code/Cline"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.config = config_manager.get_config()
        self.conversation_history: List[dict] = []
        self.agent = None
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the AI agent with configured provider"""
        # Agent will be created on first use to handle configuration errors gracefully
        self.agent = None
    
    def run(self):
        """Run the interactive prompt loop"""
        self._display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = self._get_user_input()
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if self._handle_special_commands(user_input):
                    continue
                
                # Process the message
                self._process_message(user_input)
                
            except KeyboardInterrupt:
                self._handle_interrupt()
                break
            except EOFError:
                console.print("\n👋 Goodbye!", style="blue")
                break
            except Exception as e:
                console.print(f"❌ Error: {e}", style="red")
    
    def _display_welcome(self):
        """Display welcome message"""
        provider_info = ProviderFactory.get_available_providers()[self.config.provider]
        model_name = self.config.models[self.config.provider]
        
        welcome_text = f"""
🚀 TradeArena CLI - Interactive AI Assistant

Provider: {provider_info['name']} 
Model: {model_name}
Type 'help' for commands or Ctrl+C to exit
        """.strip()
        
        console.print(Panel(
            welcome_text,
            title="[bold blue]TradeArena CLI[/bold blue]",
            border_style="blue"
        ))
    
    def _get_user_input(self) -> str:
        """Get user input with nice prompt"""
        return Prompt.ask(
            "\n[bold blue]You[/bold blue]",
            default="",
            show_default=False
        )
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """Handle special commands like help, clear, etc."""
        cmd = user_input.lower().strip()
        
        if cmd in ['help', 'h', '?']:
            self._show_help()
            return True
        elif cmd in ['clear', 'cls']:
            console.clear()
            self._display_welcome()
            return True
        elif cmd in ['exit', 'quit']:
            raise EOFError
        elif cmd == 'config':
            self._show_config()
            return True
        elif cmd == 'history':
            self._show_history()
            return True
        elif cmd.startswith('model '):
            self._switch_model(cmd[6:].strip())
            return True
        
        return False
    
    def _show_help(self):
        """Display help information"""
        help_text = """
[bold]Available Commands:[/bold]

• [cyan]help[/cyan], [cyan]h[/cyan], [cyan]?[/cyan] - Show this help
• [cyan]clear[/cyan], [cyan]cls[/cyan] - Clear the screen
• [cyan]exit[/cyan], [cyan]quit[/cyan] - Exit the CLI
• [cyan]config[/cyan] - Show current configuration
• [cyan]history[/cyan] - Show conversation history
• [cyan]model <provider>[/cyan] - Switch AI provider (bedrock, anthropic, gemini, openai)

[b]Tips:[/b]
• Use regular questions - talk to the AI naturally
• The AI has access to calculator and web search tools
• Your conversation history is preserved during the session
• Configuration is saved automatically
        """.strip()
        
        console.print(Panel(
            help_text,
            title="[bold]Help[/bold]",
            border_style="cyan"
        ))
    
    def _show_config(self):
        """Show current configuration"""
        config = self.config_manager.get_config()
        provider_info = ProviderFactory.get_available_providers()[config.provider]
        
        table = Table(title="Current Configuration")
        table.add_column("Setting", style="bold")
        table.add_column("Value")
        
        table.add_row("Provider", provider_info['name'])
        table.add_row("Model", config.models[config.provider])
        table.add_row("Temperature", str(config.params.get('temperature', 0.7)))
        table.add_row("Max Tokens", str(config.params.get('max_tokens', 1000)))
        
        console.print(table)
    
    def _show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            console.print("No conversation history yet.", style="dim")
            return
        
        console.print("\n[bold]Conversation History:[/bold]")
        for i, msg in enumerate(self.conversation_history[-10:], 1):  # Show last 10
            role = msg['role'].title()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            console.print(f"{i}. [{role}]: {content}")
    
    def _switch_model(self, provider: str):
        """Switch to a different provider"""
        if provider not in ['bedrock', 'anthropic', 'gemini', 'openai']:
            console.print(f"❌ Unknown provider: {provider}", style="red")
            console.print("Available: bedrock, anthropic, gemini, openai", style="yellow")
            return
        
        # Check if provider is configured
        if not self.config.is_configured(provider):
            console.print(f"❌ Provider '{provider}' is not configured", style="red")
            console.print("Run setup first to configure this provider.", style="yellow")
            return
        
        # Update configuration
        self.config_manager.update_config(provider=provider)
        self.config = self.config_manager.get_config()
        
        # Reset agent to force reinitialization with new provider
        self.agent = None
        provider_info = ProviderFactory.get_available_providers()[provider]
        console.print(f"✅ Switched to {provider_info['name']}", style="green")
    
    def _ensure_agent(self):
        """Ensure agent is initialized, create if needed"""
        if self.agent is None:
            try:
                from strands import Agent
                from strands_tools import calculator, http_request
                
                # Create model using provider factory
                model = ProviderFactory.create_model(self.config)
                
                # Create agent with some basic tools
                self.agent = Agent(
                    model=model,
                    tools=[calculator, http_request],
                    system_prompt=(
                        "You are an AI assistant for the TradeArena platform. "
                        "You help users with trading analysis, market research, and general questions. "
                        "You have access to calculation tools and web search. "
                        "Be helpful, accurate, and provide clear explanations."
                    )
                )
                
            except Exception as e:
                error_msg = str(e)
                if "API key" in error_msg.lower() or "authentication" in error_msg.lower():
                    console.print(f"\n❌ Authentication Error: Invalid or missing API credentials", style="red")
                    console.print("💡 Please check your configuration or run 'python3 main.py --setup' to reconfigure", style="yellow")
                elif "region" in error_msg.lower() or "bedrock" in error_msg.lower():
                    console.print(f"\n❌ AWS Configuration Error: {error_msg}", style="red")
                    console.print("💡 Please check your AWS credentials and region configuration", style="yellow")
                else:
                    console.print(f"\n❌ Provider Error: {error_msg}", style="red")
                    console.print("💡 Please check your configuration and try again", style="yellow")
                raise

    def _process_message(self, user_input: str):
        """Process user message and get AI response"""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Show thinking indicator
        with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
            try:
                # Ensure agent is initialized
                self._ensure_agent()
                
                # Get response from agent
                response = self.agent(user_input)
                response_text = str(response)
                
                # Add to conversation history
                self.conversation_history.append({"role": "assistant", "content": response_text})
                
                # Display the response
                self._display_response(response_text)
                
            except Exception as e:
                console.print(f"❌ Error getting response: {e}", style="red")
    
    def _display_response(self, response_text: str):
        """Display AI response with nice formatting"""
        console.print("\n[bold green]Assistant:[/bold green]")
        
        # Try to render as markdown if it looks like markdown
        if any(marker in response_text for marker in ['#', '```', '*', '**', '1.', '-']):
            try:
                # Handle code blocks specially
                lines = response_text.split('\n')
                in_code_block = False
                current_block = []
                
                for line in lines:
                    if line.strip().startswith('```'):
                        if in_code_block:
                            # End of code block
                            if current_block:
                                code = '\n'.join(current_block)
                                syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
                                console.print(Panel(syntax, border_style="dim"))
                            current_block = []
                            in_code_block = False
                        else:
                            # Start of code block
                            in_code_block = True
                            if line.strip() != '```':
                                # Extract language
                                lang = line.strip()[3:].strip()
                                current_block = []
                    elif in_code_block:
                        current_block.append(line)
                    else:
                        # Regular text - render as markdown
                        if line.strip():
                            md = Markdown(line)
                            console.print(md)
                        else:
                            console.print()
                
                # Handle trailing code block
                if in_code_block and current_block:
                    code = '\n'.join(current_block)
                    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
                    console.print(Panel(syntax, border_style="dim"))
                    
            except Exception:
                # Fallback to plain text
                console.print(response_text)
        else:
            # Plain text
            console.print(response_text)
        
        console.print()  # Add spacing
    
    def _handle_interrupt(self):
        """Handle Ctrl+C interrupt"""
        console.print("\n\n[yellow]Interrupted. Press Ctrl+C again to exit or Enter to continue...[/yellow]")
        try:
            # Wait for user to decide
            input()
        except KeyboardInterrupt:
            raise EOFError
