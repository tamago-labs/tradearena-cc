"""
Configure Agent Menu for TradeArena CLI
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.align import Align
from rich import box


class ConfigMenu:
    """Configure Agent menu for TradeArena CLI"""
    
    def __init__(self, console: Console, config, mock_services):
        self.console = console
        self.config = config
        self.mock_services = mock_services
    
    def run(self):
        """Run the configure agent menu"""
        while True:
            self._show_configure_agent_menu()
    
    def _show_configure_agent_menu(self):
        """Display configure agent menu"""
        self.console.clear()
        
        title = Text.from_markup(
            "[bold blue]Configure Agent[/bold blue]",
            justify="center"
        )
        
        menu_text = Text.from_markup(
            "\n❯ [bold green]AI Model[/bold green]\n"
            "  [bold green]MCP Tools[/bold green]\n"
            "  [bold green]Strategy & Risk[/bold green]\n"
            "  [bold green]HTML Interface[/bold green]\n"
            "  [bold yellow]Back[/bold yellow]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(menu_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        choice = Prompt.ask(
            "\n[bold]Enter your choice[/bold]",
            choices=["1", "2", "3", "4", "5", "model", "mcp", "strategy", "html", "back"],
            default=None
        )
        
        if choice in ["1", "model"]:
            self._ai_model_menu()
        elif choice in ["2", "mcp"]:
            self._mcp_tools_menu()
        elif choice in ["3", "strategy"]:
            self._strategy_risk_menu()
        elif choice in ["4", "html"]:
            self._html_interface_menu()
        elif choice in ["5", "back"]:
            break
    
    def _ai_model_menu(self):
        """AI Model configuration menu"""
        while True:
            self.console.clear()
            
            # Show current configuration
            current_provider = self.config.get("agent.model.provider", "OpenAI")
            current_model = self.config.get("agent.model.model", "gpt-4")
            current_temp = self.config.get("agent.model.temperature", 0.7)
            current_tokens = self.config.get("agent.model.max_tokens", 4000)
            
            title = Text.from_markup(
                "[bold blue]AI Model Configuration[/bold blue]",
                justify="center"
            )
            
            config_text = Text.from_markup(
                f"\n[bold]Current Configuration:[/bold]\n"
                f"Provider: [cyan]{current_provider}[/cyan]\n"
                f"Model: [cyan]{current_model}[/cyan]\n"
                f"Temperature: [cyan]{current_temp}[/cyan]\n"
                f"Max Tokens: [cyan]{current_tokens}[/cyan]\n"
                f"\n❯ [bold green]Change provider[/bold green]\n"
                f"  [bold green]Change model[/bold green]\n"
                f"  [bold green]Change temperature[/bold green]\n"
                f"  [bold green]Change max tokens[/bold green]\n"
                f"  [bold yellow]Back[/bold yellow]",
                justify="left"
            )
            
            panel = Panel(
                Align.center(config_text),
                title=Align.center(title),
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
            
            choice = Prompt.ask(
                "\n[bold]Enter your choice[/bold]",
                choices=["1", "2", "3", "4", "5", "provider", "model", "temp", "tokens", "back"],
                default=None
            )
            
            if choice in ["1", "provider"]:
                self._change_provider()
            elif choice in ["2", "model"]:
                self._change_model()
            elif choice in ["3", "temp"]:
                self._change_temperature()
            elif choice in ["4", "tokens"]:
                self._change_max_tokens()
            elif choice in ["5", "back"]:
                break
    
    def _change_provider(self):
        """Change AI model provider"""
        self.console.clear()
        
        self.console.print("[bold]Select AI model provider:[/bold]")
        provider = Prompt.ask(
            "Provider",
            choices=["OpenAI", "Anthropic", "DeepSeek", "Local/Custom"],
            default=self.config.get("agent.model.provider", "OpenAI")
        )
        
        self.config.set("agent.model.provider", provider)
        self.console.print(f"[bold green]Provider changed to {provider}[/bold green]")
        
        # Update model suggestion based on provider
        if provider == "OpenAI":
            suggested_model = "gpt-4"
        elif provider == "Anthropic":
            suggested_model = "claude-3-sonnet"
        elif provider == "DeepSeek":
            suggested_model = "deepseek-coder"
        else:
            suggested_model = "custom-model"
        
        if Prompt.ask(f"Use suggested model '{suggested_model}'?", choices=["y", "n"], default="y") == "y":
            self.config.set("agent.model.model", suggested_model)
            self.console.print(f"[bold green]Model set to {suggested_model}[/bold green]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _change_model(self):
        """Change AI model"""
        self.console.clear()
        
        provider = self.config.get("agent.model.provider", "OpenAI")
        current_model = self.config.get("agent.model.model", "gpt-4")
        
        if provider == "OpenAI":
            models = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
        elif provider == "Anthropic":
            models = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
        elif provider == "DeepSeek":
            models = ["deepseek-coder", "deepseek-chat"]
        else:
            models = ["custom-model"]
        
        self.console.print(f"[bold]Available models for {provider}:[/bold]")
        for i, model in enumerate(models, 1):
            marker = "❯" if model == current_model else " "
            self.console.print(f"{marker} {i}. [cyan]{model}[/cyan]")
        
        try:
            choice = int(Prompt.ask(f"Enter model number (current: {current_model})")) - 1
            if 0 <= choice < len(models):
                new_model = models[choice]
                self.config.set("agent.model.model", new_model)
                self.console.print(f"[bold green]Model changed to {new_model}[/bold green]")
            else:
                self.console.print("[red]Invalid model number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _change_temperature(self):
        """Change model temperature"""
        self.console.clear()
        
        current_temp = self.config.get("agent.model.temperature", 0.7)
        
        try:
            new_temp = float(Prompt.ask(f"Enter temperature (0.0-2.0, current: {current_temp})"))
            if 0.0 <= new_temp <= 2.0:
                self.config.set("agent.model.temperature", new_temp)
                self.console.print(f"[bold green]Temperature changed to {new_temp}[/bold green]")
            else:
                self.console.print("[red]Temperature must be between 0.0 and 2.0[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _change_max_tokens(self):
        """Change max tokens"""
        self.console.clear()
        
        current_tokens = self.config.get("agent.model.max_tokens", 4000)
        
        try:
            new_tokens = int(Prompt.ask(f"Enter max tokens (100-32000, current: {current_tokens})"))
            if 100 <= new_tokens <= 32000:
                self.config.set("agent.model.max_tokens", new_tokens)
                self.console.print(f"[bold green]Max tokens changed to {new_tokens}[/bold green]")
            else:
                self.console.print("[red]Max tokens must be between 100 and 32000[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _mcp_tools_menu(self):
        """MCP Tools configuration menu"""
        while True:
            self.console.clear()
            
            title = Text.from_markup(
                "[bold blue]MCP Tools (Execution Layer)[/bold blue]",
                justify="center"
            )
            
            menu_text = Text.from_markup(
                "\n[bold]Select ecosystem tools to enable:[/bold]\n\n"
                "❯ [bold green]Sui Tools[/bold green]\n"
                "  [bold green]KAIA Tools[/bold green]\n"
                "  [bold green]Cronos Tools[/bold green]\n"
                "  [bold yellow]Back[/bold yellow]",
                justify="left"
            )
            
            panel = Panel(
                Align.center(menu_text),
                title=Align.center(title),
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
            
            choice = Prompt.ask(
                "\n[bold]Enter your choice[/bold]",
                choices=["1", "2", "3", "4", "sui", "kaia", "cronos", "back"],
                default=None
            )
            
            if choice in ["1", "sui"]:
                self._sui_tools_menu()
            elif choice in ["2", "kaia"]:
                self._kaia_tools_menu()
            elif choice in ["3", "cronos"]:
                self._cronos_tools_menu()
            elif choice in ["4", "back"]:
                break
    
    def _sui_tools_menu(self):
        """Sui tools configuration"""
        self.console.clear()
        
        tools = {
            "navi_protocol": "Navi Protocol",
            "scallop": "Scallop",
            "validator_staking": "Validator Staking"
        }
        
        title = Text.from_markup(
            "[bold blue]Sui Tools[/bold blue]",
            justify="center"
        )
        
        self.console.print("[bold]Toggle Sui tools:[/bold]\n")
        
        for key, name in tools.items():
            enabled = self.config.get(f"agent.mcp_tools.sui.{key}", False)
            status = "[green]Enabled[/green]" if enabled else "[red]Disabled[/red]"
            self.console.print(f"{key}. {name}: {status}")
        
        tool_choice = Prompt.ask(
            "\nEnter tool number to toggle (or 'back')",
            choices=["1", "2", "3", "back"],
            default=None
        )
        
        if tool_choice == "back":
            return
        
        tool_keys = list(tools.keys())
        try:
            index = int(tool_choice) - 1
            if 0 <= index < len(tool_keys):
                key = tool_keys[index]
                current_state = self.config.get(f"agent.mcp_tools.sui.{key}", False)
                new_state = not current_state
                self.config.set(f"agent.mcp_tools.sui.{key}", new_state)
                status = "enabled" if new_state else "disabled"
                self.console.print(f"[bold green]{tools[key]} {status}[/bold green]")
        except (ValueError, IndexError):
            self.console.print("[red]Invalid choice.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _kaia_tools_menu(self):
        """KAIA tools configuration"""
        self.console.clear()
        
        tools = {
            "kilolend": "KiloLend",
            "dragonswap": "DragonSwap"
        }
        
        title = Text.from_markup(
            "[bold blue]KAIA Tools[/bold blue]",
            justify="center"
        )
        
        self.console.print("[bold]Toggle KAIA tools:[/bold]\n")
        
        for key, name in tools.items():
            enabled = self.config.get(f"agent.mcp_tools.kaia.{key}", False)
            status = "[green]Enabled[/green]" if enabled else "[red]Disabled[/red]"
            self.console.print(f"{key}. {name}: {status}")
        
        tool_choice = Prompt.ask(
            "\nEnter tool number to toggle (or 'back')",
            choices=["1", "2", "back"],
            default=None
        )
        
        if tool_choice == "back":
            return
        
        tool_keys = list(tools.keys())
        try:
            index = int(tool_choice) - 1
            if 0 <= index < len(tool_keys):
                key = tool_keys[index]
                current_state = self.config.get(f"agent.mcp_tools.kaia.{key}", False)
                new_state = not current_state
                self.config.set(f"agent.mcp_tools.kaia.{key}", new_state)
                status = "enabled" if new_state else "disabled"
                self.console.print(f"[bold green]{tools[key]} {status}[/bold green]")
        except (ValueError, IndexError):
            self.console.print("[red]Invalid choice.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _cronos_tools_menu(self):
        """Cronos tools configuration"""
        self.console.clear()
        
        tools = {
            "moonlander": "Moonlander",
            "delphi": "Delphi",
            "vvs_finance": "VVS Finance",
            "cronos_x402": "Cronos X402"
        }
        
        self.console.print("[bold]Toggle Cronos tools:[/bold]\n")
        
        for key, name in tools.items():
            enabled = self.config.get(f"agent.mcp_tools.cronos.{key}", False)
            status = "[green]Enabled[/green]" if enabled else "[red]Disabled[/red]"
            self.console.print(f"{key}. {name}: {status}")
        
        tool_choice = Prompt.ask(
            "\nEnter tool number to toggle (or 'back')",
            choices=["1", "2", "3", "4", "back"],
            default=None
        )
        
        if tool_choice == "back":
            return
        
        tool_keys = list(tools.keys())
        try:
            index = int(tool_choice) - 1
            if 0 <= index < len(tool_keys):
                key = tool_keys[index]
                current_state = self.config.get(f"agent.mcp_tools.cronos.{key}", False)
                new_state = not current_state
                self.config.set(f"agent.mcp_tools.cronos.{key}", new_state)
                status = "enabled" if new_state else "disabled"
                self.console.print(f"[bold green]{tools[key]} {status}[/bold green]")
        except (ValueError, IndexError):
            self.console.print("[red]Invalid choice.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _strategy_risk_menu(self):
        """Strategy & Risk configuration menu"""
        while True:
            self.console.clear()
            
            # Show current configuration
            current_template = self.config.get("agent.strategy.template", "balanced")
            current_position_size = self.config.get("agent.strategy.max_position_size", 1000)
            current_drawdown = self.config.get("agent.strategy.drawdown_limit", 0.1)
            
            title = Text.from_markup(
                "[bold blue]Strategy & Risk[/bold blue]",
                justify="center"
            )
            
            config_text = Text.from_markup(
                f"\n[bold]Current Configuration:[/bold]\n"
                f"Strategy Template: [cyan]{current_template}[/cyan]\n"
                f"Max Position Size: [cyan]${current_position_size}[/cyan]\n"
                f"Drawdown Limit: [cyan]{current_drawdown:.1%}[/cyan]\n"
                f"\n❯ [bold green]Select strategy template[/bold green]\n"
                f"  [bold green]Set max position size[/bold green]\n"
                f"  [bold green]Set drawdown limit[/bold green]\n"
                f"  [bold yellow]Back[/bold yellow]",
                justify="left"
            )
            
            panel = Panel(
                Align.center(config_text),
                title=Align.center(title),
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
            
            choice = Prompt.ask(
                "\n[bold]Enter your choice[/bold]",
                choices=["1", "2", "3", "4", "template", "position", "drawdown", "back"],
                default=None
            )
            
            if choice in ["1", "template"]:
                self._select_strategy_template()
            elif choice in ["2", "position"]:
                self._set_max_position_size()
            elif choice in ["3", "drawdown"]:
                self._set_drawdown_limit()
            elif choice in ["4", "back"]:
                break
    
    def _select_strategy_template(self):
        """Select strategy template"""
        self.console.clear()
        
        templates = ["conservative", "balanced", "aggressive"]
        current_template = self.config.get("agent.strategy.template", "balanced")
        
        self.console.print("[bold]Select strategy template:[/bold]\n")
        for i, template in enumerate(templates, 1):
            marker = "❯" if template == current_template else " "
            self.console.print(f"{marker} {i}. [cyan]{template.title()}[/cyan]")
        
        try:
            choice = int(Prompt.ask(f"Enter template number (current: {current_template})")) - 1
            if 0 <= choice < len(templates):
                new_template = templates[choice]
                self.config.set("agent.strategy.template", new_template)
                self.console.print(f"[bold green]Strategy template changed to {new_template}[/bold green]")
            else:
                self.console.print("[red]Invalid template number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _set_max_position_size(self):
        """Set max position size"""
        self.console.clear()
        
        current_size = self.config.get("agent.strategy.max_position_size", 1000)
        
        try:
            new_size = float(Prompt.ask(f"Enter max position size in USD (current: ${current_size})"))
            if new_size > 0:
                self.config.set("agent.strategy.max_position_size", new_size)
                self.console.print(f"[bold green]Max position size changed to ${new_size}[/bold green]")
            else:
                self.console.print("[red]Position size must be greater than 0[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _set_drawdown_limit(self):
        """Set drawdown limit"""
        self.console.clear()
        
        current_drawdown = self.config.get("agent.strategy.drawdown_limit", 0.1)
        
        try:
            new_drawdown = float(Prompt.ask(f"Enter drawdown limit as decimal (0.0-1.0, current: {current_drawdown})"))
            if 0.0 <= new_drawdown <= 1.0:
                self.config.set("agent.strategy.drawdown_limit", new_drawdown)
                self.console.print(f"[bold green]Drawdown limit changed to {new_drawdown:.1%}[/bold green]")
            else:
                self.console.print("[red]Drawdown limit must be between 0.0 and 1.0[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _html_interface_menu(self):
        """HTML Interface configuration menu"""
        while True:
            self.console.clear()
            
            # Show current configuration
            enabled = self.config.get("html_interface.enabled", True)
            port = self.config.get("html_interface.port", 5173)
            
            title = Text.from_markup(
                "[bold blue]HTML Interface (Very Important)[/bold blue]",
                justify="center"
            )
            
            explanation = "[dim]When enabled, your agent can generate and update HTML views in real time during interactive sessions.[/dim]\n"
            
            config_text = Text.from_markup(
                f"{explanation}\n"
                f"[bold]Current Configuration:[/bold]\n"
                f"Status: [cyan]{'Enabled' if enabled else 'Disabled'}[/cyan]\n"
                f"Port: [cyan]{port}[/cyan]\n"
                f"\n❯ [bold green]Enable agent-generated UI[/bold green]\n"
                f"  [bold green]Set local server port[/bold green]\n"
                f"  [bold green]Reset UI state[/bold green]\n"
                f"  [bold yellow]Back[/bold yellow]",
                justify="left"
            )
            
            panel = Panel(
                Align.center(config_text),
                title=Align.center(title),
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
            
            choice = Prompt.ask(
                "\n[bold]Enter your choice[/bold]",
                choices=["1", "2", "3", "4", "enable", "port", "reset", "back"],
                default=None
            )
            
            if choice in ["1", "enable"]:
                new_state = not enabled
                self.config.set("html_interface.enabled", new_state)
                status = "enabled" if new_state else "disabled"
                self.console.print(f"[bold green]HTML interface {status}[/bold green]")
                self.console.print("\nPress Enter to continue...")
                input()
            elif choice in ["2", "port"]:
                self._set_html_port()
            elif choice in ["3", "reset"]:
                self._reset_ui_state()
            elif choice in ["4", "back"]:
                break
    
    def _set_html_port(self):
        """Set HTML interface port"""
        self.console.clear()
        
        current_port = self.config.get("html_interface.port", 5173)
        
        try:
            new_port = int(Prompt.ask(f"Enter port number (1024-65535, current: {current_port})"))
            if 1024 <= new_port <= 65535:
                self.config.set("html_interface.port", new_port)
                self.console.print(f"[bold green]Port changed to {new_port}[/bold green]")
            else:
                self.console.print("[red]Port must be between 1024 and 65535[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _reset_ui_state(self):
        """Reset UI state"""
        self.console.clear()
        
        if Confirm.ask("[bold red]Are you sure you want to reset all UI state? This will clear all generated views.[/bold red]"):
            # In real implementation, this would clear the UI state database/files
            self.console.print("[bold green]UI state reset successfully.[/bold green]")
        else:
            self.console.print("[yellow]UI state reset cancelled.[/yellow]")
        
        self.console.print("\nPress Enter to continue...")
        input()