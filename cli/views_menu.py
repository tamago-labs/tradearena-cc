"""
Manage Views Menu for TradeArena CLI
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.align import Align
from rich import box


class ViewsMenu:
    """Manage Views menu for TradeArena CLI"""
    
    def __init__(self, console: Console, config, mock_services):
        self.console = console
        self.config = config
        self.mock_services = mock_services
    
    def run(self):
        """Run the manage views menu"""
        while True:
            if self._show_manage_views_menu():
                break
    
    def _show_manage_views_menu(self):
        """Display manage views menu"""
        self.console.clear()
        
        title = Text.from_markup(
            "[bold blue]Manage Views[/bold blue]",
            justify="center"
        )
        
        menu_text = Text.from_markup(
            "\n[bold green]1. List available views[/bold green]\n"
            "[bold green]2. View specific dashboard[/bold green]\n"
            "[bold green]3. Delete view[/bold green]\n"
            "[bold yellow]4. Back[/bold yellow]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(menu_text),
            title=title,
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        choice = Prompt.ask("\n[bold]Enter your choice (1-4)[/bold]")
        
        if choice in ["1", "list"]:
            self._list_available_views()
            return False
        elif choice in ["2", "view"]:
            self._view_specific_dashboard()
            return False
        elif choice in ["3", "delete"]:
            self._delete_view()
            return False
        elif choice in ["4", "back"]:
            return True
    
    def _list_available_views(self):
        """List all available views"""
        self.console.clear()
        
        views = self.mock_services.get_available_views()
        
        if not views:
            self.console.print("[yellow]No views available.[/yellow]")
        else:
            table = Table(title="Available Views", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Last Updated", style="blue")
            
            for view in views:
                table.add_row(
                    view["name"],
                    view["type"],
                    view["last_updated"]
                )
            
            self.console.print(table)
            
            # Show HTML interface info
            if self.config.get("html_interface.enabled", True):
                port = self.config.get("html_interface.port", 5173)
                self.console.print(f"\n[cyan]Access views at: http://localhost:{port}[/cyan]")
            else:
                self.console.print(f"\n[yellow]HTML interface is disabled. Enable it in Configure Agent > HTML Interface.[/yellow]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _view_specific_dashboard(self):
        """View a specific dashboard"""
        self.console.clear()
        
        views = self.mock_services.get_available_views()
        
        if not views:
            self.console.print("[yellow]No views available to view.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        # Show available views
        table = Table(title="Select view to open", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Last Updated", style="blue")
        
        for i, view in enumerate(views, 1):
            table.add_row(
                str(i),
                view["name"],
                view["type"],
                view["last_updated"]
            )
        
        self.console.print(table)
        
        # Get view to open
        try:
            choice = int(Prompt.ask("Enter view number to open")) - 1
            if 0 <= choice < len(views):
                view = views[choice]
                
                # Check if HTML interface is enabled
                if not self.config.get("html_interface.enabled", True):
                    self.console.print("[yellow]HTML interface is disabled. Enabling it now...[/yellow]")
                    self.config.set("html_interface.enabled", True)
                    self.console.print("[green]HTML interface enabled.[/green]")
                
                port = self.config.get("html_interface.port", 5173)
                self.console.print(f"[bold green]Opening '{view['name']}' in browser...[/bold green]")
                self.console.print(f"[cyan]URL: http://localhost:{port}/view/{view['name'].lower().replace(' ', '_')}[/cyan]")
                
                # In real implementation, this would open the browser
                # For now, just show the URL
                self.console.print("\n[dim](In production, this would automatically open your browser)[/dim]")
            else:
                self.console.print("[red]Invalid view number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _delete_view(self):
        """Delete a view"""
        self.console.clear()
        
        views = self.mock_services.get_available_views()
        
        if not views:
            self.console.print("[yellow]No views available to delete.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        # Show available views
        table = Table(title="Select view to delete", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Last Updated", style="blue")
        
        for i, view in enumerate(views, 1):
            table.add_row(
                str(i),
                view["name"],
                view["type"],
                view["last_updated"]
            )
        
        self.console.print(table)
        
        # Get view to delete
        try:
            choice = int(Prompt.ask("Enter view number to delete")) - 1
            if 0 <= choice < len(views):
                view = views[choice]
                
                # Confirm deletion
                if Confirm.ask(f"[bold red]Are you sure you want to delete '{view['name']}'?[/bold red]"):
                    # In real implementation, this would delete the view file/database entry
                    self.console.print(f"[bold green]View '{view['name']}' deleted successfully.[/bold green]")
                else:
                    self.console.print("[yellow]Deletion cancelled.[/yellow]")
            else:
                self.console.print("[red]Invalid view number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
        
