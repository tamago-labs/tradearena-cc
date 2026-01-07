"""
Walrus Settings Menu for TradeArena CLI
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.align import Align
from rich import box


class WalrusMenu:
    """Walrus Settings menu for TradeArena CLI"""
    
    def __init__(self, console: Console, config, mock_services):
        self.console = console
        self.config = config
        self.mock_services = mock_services
    
    def run(self):
        """Run the walrus settings menu"""
        while True:
            self._show_walrus_settings_menu()
    
    def _show_walrus_settings_menu(self):
        """Display walrus settings menu"""
        self.console.clear()
        
        # Show current configuration
        enabled = self.config.get("walrus.enabled", False)
        visibility = self.config.get("walrus.visibility", "private")
        
        title = Text.from_markup(
            "[bold blue]Walrus Settings[/bold blue]",
            justify="center"
        )
        
        config_text = Text.from_markup(
            f"\n[bold]Current Configuration:[/bold]\n"
            f"Status: [cyan]{'Enabled' if enabled else 'Disabled'}[/cyan]\n"
            f"Visibility: [cyan]{visibility.title()}[/cyan]\n"
            f"\n❯ [bold green]Enable Walrus storage[/bold green]\n"
            f"  [bold green]Disable Walrus storage[/bold green]\n"
            f"  [bold green]Set visibility (public / private)[/bold green]\n"
            f"  [bold green]View stored records[/bold green]\n"
            f"  [bold yellow]Back[/bold yellow]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(config_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        choice = Prompt.ask(
            "\n[bold]Enter your choice[/bold]",
            choices=["1", "2", "3", "4", "5", "enable", "disable", "visibility", "records", "back"],
            default=None
        )
        
        if choice in ["1", "enable"]:
            self._enable_walrus_storage()
        elif choice in ["2", "disable"]:
            self._disable_walrus_storage()
        elif choice in ["3", "visibility"]:
            self._set_visibility()
        elif choice in ["4", "records"]:
            self._view_stored_records()
        elif choice in ["5", "back"]:
            break
    
    def _enable_walrus_storage(self):
        """Enable Walrus storage"""
        self.console.clear()
        
        # Check if already enabled
        if self.config.get("walrus.enabled", False):
            self.console.print("[yellow]Walrus storage is already enabled.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        # Show information about Walrus
        title = Text.from_markup(
            "[bold blue]Enable Walrus Storage[/bold blue]",
            justify="center"
        )
        
        info_text = Text.from_markup(
            "\n[bold]About Walrus Storage:[/bold]\n"
            "• Store and retrieve AI trade decisions and reasoning\n"
            "• Decentralized storage for transparency and auditability\n"
            "• Share insights with your team or keep them private\n"
            "• Persistent storage that survives agent restarts\n\n"
            "[bold]Configuration Options:[/bold]\n"
            "• [green]Public[/green]: Anyone with the link can view stored data\n"
            "• [red]Private[/red]: Only you can access stored data\n\n"
            "[dim]This avoids storage lock-in while still highlighting Walrus value.[/dim]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Ask for confirmation
        if Confirm.ask("\n[bold green]Do you want to enable Walrus storage?[/bold green]"):
            # Ask for visibility preference
            visibility = Prompt.ask(
                "Set default visibility",
                choices=["public", "private"],
                default="private"
            )
            
            # Enable Walrus storage
            self.config.set("walrus.enabled", True)
            self.config.set("walrus.visibility", visibility)
            
            self.console.print(f"[bold green]Walrus storage enabled with {visibility} visibility.[/bold green]")
            self.console.print("\n[dim]Your agent will now automatically store trade decisions and reasoning to Walrus.[/dim]")
        else:
            self.console.print("[yellow]Walrus storage remains disabled.[/yellow]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _disable_walrus_storage(self):
        """Disable Walrus storage"""
        self.console.clear()
        
        # Check if already disabled
        if not self.config.get("walrus.enabled", False):
            self.console.print("[yellow]Walrus storage is already disabled.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        # Show warning
        title = Text.from_markup(
            "[bold red]Disable Walrus Storage[/bold red]",
            justify="center"
        )
        
        warning_text = Text.from_markup(
            "\n[bold red]Warning:[/bold red]\n"
            "• Disabling Walrus storage will stop saving new trade decisions\n"
            "• Existing stored records will remain accessible\n"
            "• You can re-enable Walrus storage at any time\n"
            "• No data will be lost, only future storage will be affected\n\n"
            "[dim]This is an explicit opt-out to maintain user control.[/dim]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(warning_text),
            title=Align.center(title),
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Ask for confirmation
        if Confirm.ask("\n[bold red]Are you sure you want to disable Walrus storage?[/bold red]"):
            # Disable Walrus storage
            self.config.set("walrus.enabled", False)
            
            self.console.print("[bold green]Walrus storage disabled.[/bold green]")
            self.console.print("\n[dim]Your agent will no longer store trade decisions to Walrus.[/dim]")
        else:
            self.console.print("[yellow]Walrus storage remains enabled.[/yellow]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _set_visibility(self):
        """Set Walrus storage visibility"""
        self.console.clear()
        
        # Check if Walrus is enabled
        if not self.config.get("walrus.enabled", False):
            self.console.print("[yellow]Walrus storage is not enabled. Please enable it first.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        current_visibility = self.config.get("walrus.visibility", "private")
        
        title = Text.from_markup(
            "[bold blue]Set Walrus Visibility[/bold blue]",
            justify="center"
        )
        
        info_text = Text.from_markup(
            f"\n[bold]Current visibility: [cyan]{current_visibility.title()}[/cyan][/bold]\n\n"
            "[bold]Visibility Options:[/bold]\n\n"
            "❯ [bold green]Public[/bold green]\n"
            "   Anyone with the link can view stored data\n"
            "   Useful for team collaboration and transparency\n"
            "   Data is discoverable and shareable\n\n"
            "  [bold red]Private[/bold red]\n"
            "   Only you can access stored data\n"
            "   Maximum privacy and security\n"
            "   Data is encrypted and access-controlled\n\n"
            "[dim]You can change this setting at any time.[/dim]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Get new visibility setting
        new_visibility = Prompt.ask(
            f"\nSelect visibility (current: {current_visibility})",
            choices=["public", "private"],
            default=current_visibility
        )
        
        if new_visibility != current_visibility:
            self.config.set("walrus.visibility", new_visibility)
            self.console.print(f"[bold green]Visibility changed to {new_visibility}.[/bold green]")
            
            # Show additional info based on new setting
            if new_visibility == "public":
                self.console.print("\n[dim]Your stored trade decisions will be publicly accessible.[/dim]")
            else:
                self.console.print("\n[dim]Your stored trade decisions will be private and secure.[/dim]")
        else:
            self.console.print("[yellow]Visibility unchanged.[/yellow]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _view_stored_records(self):
        """View stored Walrus records"""
        self.console.clear()
        
        # Check if Walrus is enabled
        if not self.config.get("walrus.enabled", False):
            self.console.print("[yellow]Walrus storage is not enabled. Please enable it first.[/yellow]")
            self.console.print("\nPress Enter to continue...")
            input()
            return
        
        # Get stored records
        records = self.mock_services.get_walrus_records()
        visibility = self.config.get("walrus.visibility", "private")
        
        title = Text.from_markup(
            "[bold blue]Walrus Stored Records[/bold blue]",
            justify="center"
        )
        
        if not records:
            info_text = Text.from_markup(
                f"\n[yellow]No stored records found.[/yellow]\n\n"
                f"[dim]Records will appear here as your agent makes trade decisions and stores them to Walrus.[/dim]\n"
                f"[dim]Current visibility: [cyan]{visibility}[/cyan][/dim]",
                justify="left"
            )
        else:
            # Create table for records
            table = Table(title=f"Stored Records (Visibility: {visibility.title()})", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Timestamp", style="blue")
            table.add_column("Size", style="yellow")
            
            for record in records:
                table.add_row(
                    record["id"],
                    record["type"],
                    record["timestamp"],
                    record["size"]
                )
            
            self.console.print(table)
            
            # Show additional info
            info_text = Text.from_markup(
                f"\n[bold]Storage Information:[/bold]\n"
                f"Total Records: [cyan]{len(records)}[/cyan]\n"
                f"Visibility: [cyan]{visibility.title()}[/cyan]\n"
                f"Storage Location: [cyan]Walrus Network[/cyan]\n\n"
                f"[dim]Records are automatically stored during agent sessions.[/dim]",
                justify="left"
            )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Offer additional options if records exist
        if records:
            action = Prompt.ask(
                "\n[bold]Select action[/bold]",
                choices=["view", "export", "delete", "back"],
                default="back"
            )
            
            if action == "view":
                self._view_record_details()
            elif action == "export":
                self._export_records()
            elif action == "delete":
                self._delete_record()
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _view_record_details(self):
        """View details of a specific record"""
        self.console.clear()
        
        records = self.mock_services.get_walrus_records()
        
        if not records:
            return
        
        # Show records for selection
        table = Table(title="Select record to view", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Timestamp", style="blue")
        
        for i, record in enumerate(records, 1):
            table.add_row(
                str(i),
                record["id"],
                record["type"],
                record["timestamp"]
            )
        
        self.console.print(table)
        
        try:
            choice = int(Prompt.ask("Enter record number to view")) - 1
            if 0 <= choice < len(records):
                record = records[choice]
                
                # Mock record details
                self.console.print(f"\n[bold]Record Details:[/bold]")
                self.console.print(f"ID: [cyan]{record['id']}[/cyan]")
                self.console.print(f"Type: [green]{record['type']}[/green]")
                self.console.print(f"Timestamp: [blue]{record['timestamp']}[/blue]")
                self.console.print(f"Size: [yellow]{record['size']}[/yellow]")
                self.console.print(f"Storage: [cyan]Walrus Network[/cyan]")
                
                # Mock content preview
                if record["type"] == "trade_decision":
                    content = "Action: BUY\nAsset: ETH\nAmount: 1.5\nPrice: $2,450\nReasoning: Bullish momentum detected..."
                elif record["type"] == "analysis":
                    content = "Market Analysis: BTC\nIndicators: RSI oversold, MACD bullish\nRecommendation: Accumulate..."
                else:
                    content = "Portfolio Value: $45,230\nPositions: 5\nPerformance: +12.3%..."
                
                self.console.print(f"\n[dim]Content Preview:[/dim]")
                self.console.print(f"[dim]{content}[/dim]")
                
            else:
                self.console.print("[red]Invalid record number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _export_records(self):
        """Export records to file"""
        self.console.clear()
        
        visibility = self.config.get("walrus.visibility", "private")
        
        self.console.print("[bold]Export Records[/bold]\n")
        self.console.print(f"Export format: [cyan]JSON[/cyan]")
        self.console.print(f"Visibility: [cyan]{visibility.title()}[/cyan]")
        
        filename = Prompt.ask("Enter filename (without extension)", default="trade_records")
        
        # Mock export
        self.console.print(f"[bold green]Records exported to {filename}.json[/bold green]")
        self.console.print(f"[dim]Exported {len(self.mock_services.get_walrus_records())} records.[/dim]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _delete_record(self):
        """Delete a specific record"""
        self.console.clear()
        
        records = self.mock_services.get_walrus_records()
        
        if not records:
            return
        
        # Show records for selection
        table = Table(title="Select record to delete", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Timestamp", style="blue")
        
        for i, record in enumerate(records, 1):
            table.add_row(
                str(i),
                record["id"],
                record["type"],
                record["timestamp"]
            )
        
        self.console.print(table)
        
        try:
            choice = int(Prompt.ask("Enter record number to delete")) - 1
            if 0 <= choice < len(records):
                record = records[choice]
                
                # Confirm deletion
                if Confirm.ask(f"[bold red]Are you sure you want to delete record {record['id']}?[/bold red]"):
                    # In real implementation, this would delete from Walrus
                    self.console.print(f"[bold green]Record {record['id']} deleted successfully.[/bold green]")
                else:
                    self.console.print("[yellow]Deletion cancelled.[/yellow]")
            else:
                self.console.print("[red]Invalid record number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()