"""
Main Menu System for TradeArena CLI
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich import box
import sys
from typing import Optional, Callable, Dict, List

from .utils import ConfigManager, MockServices


class MenuSystem:
    """Main menu system for TradeArena CLI"""
    
    def __init__(self):
        self.console = Console()
        self.config = ConfigManager()
        self.mock_services = MockServices()
        self.running = True
    
    def run(self):
        """Start the main menu loop"""
        while self.running:
            self._show_main_menu()
    
    def _show_main_menu(self):
        """Display main menu and get user selection"""
        self.console.clear()
        
        # Create main title
        title = Text.from_markup(
            "[bold blue]Welcome to TradeArena[/bold blue]\n"
            "[dim]The Vibe Trading Arena for DeFi[/dim]",
            justify="center"
        )
        
        # Create menu options
        menu_text = Text.from_markup(
            "\n[bold]What would you like to do?[/bold]\n\n"
            "[bold cyan]1.[/bold cyan] [bold green]Interactive mode[/bold green]\n"
            "[bold cyan]2.[/bold cyan] [bold green]Scheduled mode[/bold green]\n"
            "[bold cyan]3.[/bold cyan] [bold green]Manage Views[/bold green]\n"
            "[bold cyan]4.[/bold cyan] [bold green]Configure Agent[/bold green]\n"
            "[bold cyan]5.[/bold cyan] [bold green]Walrus Settings[/bold green]\n"
            "[bold cyan]6.[/bold cyan] [bold green]Agent Logs[/bold green]\n"
            "[bold cyan]7.[/bold cyan] [bold red]Exit[/bold red]",
            justify="left"
        )
        
        # Display the panel
        panel = Panel(
            menu_text,
            title=title,
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Get user choice
        choice = Prompt.ask("\n[bold]Enter your choice (1-7)[/bold]")
        
        # Handle the choice
        self._handle_main_menu_choice(choice)
    
    def _handle_main_menu_choice(self, choice: str):
        """Handle main menu selection"""
        choice = choice.lower()
        
        if choice in ["1", "interactive"]:
            self._interactive_mode_menu()
        elif choice in ["2", "scheduled"]:
            self._scheduled_mode_menu()
        elif choice in ["3", "views"]:
            self._manage_views_menu()
        elif choice in ["4", "configure"]:
            self._configure_agent_menu()
        elif choice in ["5", "walrus"]:
            self._walrus_settings_menu()
        elif choice in ["6", "logs"]:
            self._agent_logs_menu()
        elif choice in ["7", "exit"]:
            self.running = False
            self.console.print("[bold green]Goodbye![/bold green]")
        else:
            self.console.print("[red]Invalid choice. Please try again.[/red]")
            self.console.print("Press Enter to continue...")
            input()
    
    def _interactive_mode_menu(self):
        """Interactive mode menu"""
        while True:
            self.console.clear()
            
            title = Text.from_markup(
                "[bold blue]Interactive mode[/bold blue]",
                justify="center"
            )
            
            menu_text = Text.from_markup(
                "\n[bold cyan]1.[/bold cyan] [bold green]Start a new session[/bold green]\n"
                "[bold cyan]2.[/bold cyan] [bold green]Resume last session[/bold green]\n"
                "[bold cyan]3.[/bold cyan] [bold yellow]Back[/bold yellow]",
                justify="left"
            )
            
            panel = Panel(
                menu_text,
                title=title,
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
            
            choice = Prompt.ask("\n[bold]Enter your choice (1-3)[/bold]")
            
            if choice in ["1", "new"]:
                self._start_new_session()
                break
            elif choice in ["2", "resume"]:
                self._resume_last_session()
                break
            elif choice in ["3", "back"]:
                break
    
    def _start_new_session(self):
        """Start a new interactive session"""
        self.console.clear()
        
        # Start the mock session
        result = self.mock_services.start_agent_session("new")
        
        self.console.print(f"[bold green]{result}[/bold green]")
        self.console.print()
        
        # Show session info
        self.console.print("[bold]Session Information:[/bold]")
        self.console.print("• Agent can analyze markets and execute trades")
        self.console.print("• Agent can generate custom dashboards and views")
        self.console.print("• Local HTML server started for visualization")
        self.console.print()
        
        # Simulate server info
        port = self.config.get("html_interface.port", 5173)
        self.console.print(f"[bold cyan]Local dashboard available at http://localhost:{port}[/bold cyan]")
        self.console.print()
        
        self.console.print("[bold yellow]Press Ctrl+C to stop the session[/bold yellow]")
        
        # Simulate running session (in real implementation, this would be an actual agent loop)
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            self.console.print("\n[bold green]Session stopped.[/bold green]")
            self.console.print("Press Enter to continue...")
            input()
    
    def _resume_last_session(self):
        """Resume the last session"""
        self.console.clear()
        
        result = self.mock_services.start_agent_session("resume")
        self.console.print(f"[bold green]{result}[/bold green]")
        self.console.print()
        
        port = self.config.get("html_interface.port", 5173)
        self.console.print(f"[bold cyan]Local dashboard available at http://localhost:{port}[/bold cyan]")
        self.console.print()
        
        self.console.print("Press Enter to continue...")
        input()
    
    def _scheduled_mode_menu(self):
        """Scheduled mode menu"""
        while True:
            self.console.clear()
            
            title = Text.from_markup(
                "[bold blue]Scheduled mode[/bold blue]",
                justify="center"
            )
            
            menu_text = Text.from_markup(
                "\n[bold cyan]1.[/bold cyan] [bold green]Create new schedule[/bold green]\n"
                "[bold cyan]2.[/bold cyan] [bold green]View running agents[/bold green]\n"
                "[bold cyan]3.[/bold cyan] [bold green]Stop agent[/bold green]\n"
                "[bold cyan]4.[/bold cyan] [bold yellow]Back[/bold yellow]",
                justify="left"
            )
            
            panel = Panel(
                menu_text,
                title=title,
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
            
            choice = Prompt.ask("\n[bold]Enter your choice (1-4)[/bold]")
            
            if choice in ["1", "create"]:
                self._create_new_schedule()
            elif choice in ["2", "view"]:
                self._view_running_agents()
            elif choice in ["3", "stop"]:
                self._stop_agent()
            elif choice in ["4", "back"]:
                break
    
    def _create_new_schedule(self):
        """Create a new scheduled agent"""
        self.console.clear()
        
        self.console.print("[bold]Select run mode:[/bold]")
        run_mode = Prompt.ask(
            "Run mode",
            choices=["time", "event"],
            default="time"
        )
        
        if run_mode == "time":
            schedule_type = Prompt.ask(
                "Schedule type",
                choices=["minutes", "hourly", "daily", "cron"],
                default="minutes"
            )
            
            if schedule_type == "minutes":
                interval = Prompt.ask("Enter interval in minutes", default="5")
                schedule_config = {"type": "time", "interval_minutes": int(interval)}
            elif schedule_type == "hourly":
                schedule_config = {"type": "time", "interval_hours": 1}
            elif schedule_type == "daily":
                schedule_config = {"type": "time", "interval_days": 1}
            else:  # cron
                cron_expr = Prompt.ask("Enter cron expression", default="0 */5 * * *")
                schedule_config = {"type": "cron", "expression": cron_expr}
        else:  # event-based
            trigger = Prompt.ask(
                "Event trigger",
                choices=["price_threshold", "volatility", "protocol_event"],
                default="price_threshold"
            )
            schedule_config = {"type": "event", "trigger": trigger}
        
        # Start the scheduled agent
        result = self.mock_services.start_scheduled_agent(schedule_config)
        self.console.print(f"[bold green]{result}[/bold green]")
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _view_running_agents(self):
        """View running agents"""
        self.console.clear()
        
        agents = self.mock_services.get_running_agents()
        
        if not agents:
            self.console.print("[yellow]No running agents found.[/yellow]")
        else:
            table = Table(title="Running Agents", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Schedule", style="blue")
            
            for agent in agents:
                status_style = "green" if agent["status"] == "running" else "red"
                table.add_row(
                    agent["id"],
                    agent["name"],
                    f"[{status_style}]{agent['status']}[/{status_style}]",
                    agent["schedule"]
                )
            
            self.console.print(table)
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _stop_agent(self):
        """Stop a running agent"""
        self.console.clear()
        
        agents = self.mock_services.get_running_agents()
        
        if not agents:
            self.console.print("[yellow]No running agents to stop.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        # Show running agents
        table = Table(title="Select agent to stop", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        
        for i, agent in enumerate(agents, 1):
            status_style = "green" if agent["status"] == "running" else "red"
            table.add_row(
                str(i),
                agent["id"],
                agent["name"],
                f"[{status_style}]{agent['status']}[/{status_style}]"
            )
        
        self.console.print(table)
        
        # Get agent to stop
        try:
            choice = int(Prompt.ask("Enter agent number to stop")) - 1
            if 0 <= choice < len(agents):
                agent = agents[choice]
                self.console.print(f"[bold green]Agent {agent['name']} ({agent['id']}) stopped.[/bold green]")
            else:
                self.console.print("[red]Invalid agent number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _manage_views_menu(self):
        """Manage views menu"""
        from .views_menu import ViewsMenu
        views_menu = ViewsMenu(self.console, self.config, self.mock_services)
        views_menu.run()
    
    def _configure_agent_menu(self):
        """Configure agent menu"""
        from .config_menu import ConfigMenu
        config_menu = ConfigMenu(self.console, self.config, self.mock_services)
        config_menu.run()
    
    def _walrus_settings_menu(self):
        """Walrus settings menu"""
        from .walrus_menu import WalrusMenu
        walrus_menu = WalrusMenu(self.console, self.config, self.mock_services)
        walrus_menu.run()
    
    def _agent_logs_menu(self):
        """Agent logs menu"""
        from .logs_menu import LogsMenu
        logs_menu = LogsMenu(self.console, self.config, self.mock_services)
        logs_menu.run()
