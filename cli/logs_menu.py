"""
Agent Logs Menu for TradeArena CLI
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.align import Align
from rich import box
from rich.syntax import Syntax
from datetime import datetime, timedelta
import json


class LogsMenu:
    """Agent Logs menu for TradeArena CLI"""
    
    def __init__(self, console: Console, config, mock_services):
        self.console = console
        self.config = config
        self.mock_services = mock_services
    
    def run(self):
        """Run the agent logs menu"""
        while True:
            self._show_agent_logs_menu()
    
    def _show_agent_logs_menu(self):
        """Display agent logs menu"""
        self.console.clear()
        
        title = Text.from_markup(
            "[bold blue]Agent Logs[/bold blue]",
            justify="center"
        )
        
        menu_text = Text.from_markup(
            "\n❯ [bold green]View recent trades[/bold green]\n"
            "  [bold green]View decision history[/bold green]\n"
            "  [bold green]Export logs[/bold green]\n"
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
            choices=["1", "2", "3", "4", "trades", "decisions", "export", "back"],
            default=None
        )
        
        if choice in ["1", "trades"]:
            self._view_recent_trades()
        elif choice in ["2", "decisions"]:
            self._view_decision_history()
        elif choice in ["3", "export"]:
            self._export_logs()
        elif choice in ["4", "back"]:
            break
    
    def _view_recent_trades(self):
        """View recent trades"""
        self.console.clear()
        
        # Get mock trade logs
        trades = self.mock_services.get_agent_logs()
        
        title = Text.from_markup(
            "[bold blue]Recent Trades[/bold blue]",
            justify="center"
        )
        
        if not trades:
            info_text = Text.from_markup(
                "\n[yellow]No recent trades found.[/yellow]\n\n"
                "[dim]Trades will appear here as your agent executes them during sessions.[/dim]",
                justify="left"
            )
        else:
            # Create trades table
            table = Table(title="Recent Trade Activity", box=box.ROUNDED)
            table.add_column("Timestamp", style="blue")
            table.add_column("Action", style="green")
            table.add_column("Token", style="cyan")
            table.add_column("Amount", style="yellow")
            table.add_column("Price", style="magenta")
            
            for trade in trades:
                # Color code actions
                action_style = "green" if trade["action"] == "BUY" else "red" if trade["action"] == "SELL" else "blue"
                
                table.add_row(
                    trade["timestamp"],
                    f"[{action_style}]{trade['action']}[/{action_style}]",
                    trade["token"],
                    str(trade["amount"]),
                    f"${trade['price']:,.2f}" if isinstance(trade["price"], (int, float)) else str(trade["price"])
                )
            
            self.console.print(table)
            
            # Calculate some statistics
            total_trades = len(trades)
            buy_trades = len([t for t in trades if t["action"] == "BUY"])
            sell_trades = len([t for t in trades if t["action"] == "SELL"])
            stake_trades = len([t for t in trades if t["action"] == "STAKE"])
            
            info_text = Text.from_markup(
                f"\n[bold]Trade Summary:[/bold]\n"
                f"Total Trades: [cyan]{total_trades}[/cyan]\n"
                f"Buy Orders: [green]{buy_trades}[/green]\n"
                f"Sell Orders: [red]{sell_trades}[/red]\n"
                f"Stake Operations: [blue]{stake_trades}[/blue]\n\n"
                f"[dim]Most recent activity shown from the last 24 hours.[/dim]",
                justify="left"
            )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Offer additional options if trades exist
        if trades:
            action = Prompt.ask(
                "\n[bold]Select action[/bold]",
                choices=["details", "filter", "export", "back"],
                default="back"
            )
            
            if action == "details":
                self._view_trade_details(trades)
            elif action == "filter":
                self._filter_trades()
            elif action == "export":
                self._export_trades(trades)
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _view_trade_details(self, trades):
        """View details of a specific trade"""
        self.console.clear()
        
        # Show trades for selection
        table = Table(title="Select trade for details", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("Timestamp", style="blue")
        table.add_column("Action", style="green")
        table.add_column("Token", style="cyan")
        table.add_column("Amount", style="yellow")
        
        for i, trade in enumerate(trades, 1):
            action_style = "green" if trade["action"] == "BUY" else "red" if trade["action"] == "SELL" else "blue"
            table.add_row(
                str(i),
                trade["timestamp"],
                f"[{action_style}]{trade['action']}[/{action_style}]",
                trade["token"],
                str(trade["amount"])
            )
        
        self.console.print(table)
        
        try:
            choice = int(Prompt.ask("Enter trade number for details")) - 1
            if 0 <= choice < len(trades):
                trade = trades[choice]
                
                # Detailed trade information
                self.console.print(f"\n[bold]Trade Details:[/bold]")
                self.console.print(f"Timestamp: [blue]{trade['timestamp']}[/blue]")
                
                action_style = "green" if trade["action"] == "BUY" else "red" if trade["action"] == "SELL" else "blue"
                self.console.print(f"Action: [{action_style}]{trade['action']}[/{action_style}]")
                self.console.print(f"Token: [cyan]{trade['token']}[/cyan]")
                self.console.print(f"Amount: [yellow]{trade['amount']}[/yellow]")
                self.console.print(f"Price: [magenta]${trade['price']:,.2f}[/magenta]" if isinstance(trade["price"], (int, float)) else f"Price: [magenta]{trade['price']}[/magenta]")
                
                # Calculate total value
                if isinstance(trade["price"], (int, float)):
                    total_value = trade["amount"] * trade["price"]
                    self.console.print(f"Total Value: [green]${total_value:,.2f}[/green]")
                
                # Mock additional details based on action type
                if trade["action"] == "BUY":
                    self.console.print(f"\n[dim]Buy Reason: Market momentum positive, RSI indicating oversold condition[/dim]")
                    self.console.print(f"[dim]Expected Outcome: Short-term price appreciation[/dim]")
                elif trade["action"] == "SELL":
                    self.console.print(f"\n[dim]Sell Reason: Profit target reached, technical resistance at current level[/dim]")
                    self.console.print(f"[dim]Expected Outcome: Position consolidation[/dim]")
                elif trade["action"] == "STAKE":
                    self.console.print(f"\n[dim]Stake Reason: High validator performance, attractive APY[/dim]")
                    self.console.print(f"[dim]Expected Outcome: Passive income generation[/dim]")
                    self.console.print(f"Validator: [cyan]{trade.get('validator', 'N/A')}[/cyan]")
                
                # Mock execution details
                self.console.print(f"\n[bold]Execution Details:[/bold]")
                self.console.print(f"Exchange: [cyan]Decentralized Exchange[/cyan]")
                self.console.print(f"Gas Used: [yellow]0.0025 ETH[/yellow]")
                self.console.print(f"Transaction Hash: [dim]0x7f9a...3b2c[/dim]")
                self.console.print(f"Status: [green]Completed[/green]")
                
            else:
                self.console.print("[red]Invalid trade number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _filter_trades(self):
        """Filter trades by criteria"""
        self.console.clear()
        
        title = Text.from_markup(
            "[bold blue]Filter Trades[/bold blue]",
            justify="center"
        )
        
        info_text = Text.from_markup(
            "\n[bold]Filter Options:[/bold]\n"
            "❯ [bold green]Filter by action type[/bold green]\n"
            "  [bold green]Filter by token[/bold green]\n"
            "  [bold green]Filter by time range[/bold green]\n"
            "  [bold green]Filter by value range[/bold green]\n"
            "  [bold yellow]Back[/bold yellow]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        filter_type = Prompt.ask(
            "\n[bold]Select filter type[/bold]",
            choices=["1", "2", "3", "4", "5", "action", "token", "time", "value", "back"],
            default=None
        )
        
        if filter_type in ["1", "action"]:
            self._filter_by_action()
        elif filter_type in ["2", "token"]:
            self._filter_by_token()
        elif filter_type in ["3", "time"]:
            self._filter_by_time()
        elif filter_type in ["4", "value"]:
            self._filter_by_value()
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _filter_by_action(self):
        """Filter trades by action type"""
        self.console.clear()
        
        action = Prompt.ask(
            "Select action type",
            choices=["BUY", "SELL", "STAKE"],
            default="BUY"
        )
        
        trades = self.mock_services.get_agent_logs()
        filtered_trades = [t for t in trades if t["action"] == action]
        
        self.console.print(f"\n[bold]Trades with action '{action}':[/bold]")
        
        if filtered_trades:
            table = Table(box=box.ROUNDED)
            table.add_column("Timestamp", style="blue")
            table.add_column("Token", style="cyan")
            table.add_column("Amount", style="yellow")
            table.add_column("Price", style="magenta")
            
            for trade in filtered_trades:
                table.add_row(
                    trade["timestamp"],
                    trade["token"],
                    str(trade["amount"]),
                    f"${trade['price']:,.2f}" if isinstance(trade["price"], (int, float)) else str(trade["price"])
                )
            
            self.console.print(table)
            self.console.print(f"\n[dim]Found {len(filtered_trades)} matching trades.[/dim]")
        else:
            self.console.print("[yellow]No trades found with this action type.[/yellow]")
    
    def _filter_by_token(self):
        """Filter trades by token"""
        self.console.clear()
        
        token = Prompt.ask("Enter token symbol", default="ETH").upper()
        
        trades = self.mock_services.get_agent_logs()
        filtered_trades = [t for t in trades if t["token"].upper() == token]
        
        self.console.print(f"\n[bold]Trades for token '{token}':[/bold]")
        
        if filtered_trades:
            table = Table(box=box.ROUNDED)
            table.add_column("Timestamp", style="blue")
            table.add_column("Action", style="green")
            table.add_column("Amount", style="yellow")
            table.add_column("Price", style="magenta")
            
            for trade in filtered_trades:
                action_style = "green" if trade["action"] == "BUY" else "red" if trade["action"] == "SELL" else "blue"
                table.add_row(
                    trade["timestamp"],
                    f"[{action_style}]{trade['action']}[/{action_style}]",
                    str(trade["amount"]),
                    f"${trade['price']:,.2f}" if isinstance(trade["price"], (int, float)) else str(trade["price"])
                )
            
            self.console.print(table)
            self.console.print(f"\n[dim]Found {len(filtered_trades)} matching trades.[/dim]")
        else:
            self.console.print(f"[yellow]No trades found for token '{token}'.[/yellow]")
    
    def _filter_by_time(self):
        """Filter trades by time range"""
        self.console.clear()
        
        time_range = Prompt.ask(
            "Select time range",
            choices=["1h", "6h", "24h", "7d", "30d"],
            default="24h"
        )
        
        trades = self.mock_services.get_agent_logs()
        
        # Mock time filtering (in real implementation, this would filter by actual timestamps)
        if time_range == "1h":
            filtered_trades = trades[:1] if trades else []
        elif time_range == "6h":
            filtered_trades = trades[:2] if trades else []
        elif time_range == "24h":
            filtered_trades = trades
        elif time_range == "7d":
            filtered_trades = trades * 2 if trades else []  # Mock more data
        else:  # 30d
            filtered_trades = trades * 3 if trades else []  # Mock even more data
        
        self.console.print(f"\n[bold]Trades in the last {time_range}:[/bold]")
        
        if filtered_trades:
            table = Table(box=box.ROUNDED)
            table.add_column("Timestamp", style="blue")
            table.add_column("Action", style="green")
            table.add_column("Token", style="cyan")
            table.add_column("Amount", style="yellow")
            
            for trade in filtered_trades:
                action_style = "green" if trade["action"] == "BUY" else "red" if trade["action"] == "SELL" else "blue"
                table.add_row(
                    trade["timestamp"],
                    f"[{action_style}]{trade['action']}[/{action_style}]",
                    trade["token"],
                    str(trade["amount"])
                )
            
            self.console.print(table)
            self.console.print(f"\n[dim]Found {len(filtered_trades)} matching trades.[/dim]")
        else:
            self.console.print(f"[yellow]No trades found in the last {time_range}.[/yellow]")
    
    def _filter_by_value(self):
        """Filter trades by value range"""
        self.console.clear()
        
        try:
            min_value = float(Prompt.ask("Enter minimum value in USD", default="0"))
            max_value = float(Prompt.ask("Enter maximum value in USD", default="100000"))
        except ValueError:
            self.console.print("[red]Please enter valid numbers.[/red]")
            return
        
        trades = self.mock_services.get_agent_logs()
        filtered_trades = []
        
        for trade in trades:
            if isinstance(trade["price"], (int, float)):
                value = trade["amount"] * trade["price"]
                if min_value <= value <= max_value:
                    filtered_trades.append(trade)
        
        self.console.print(f"\n[bold]Trades with value between ${min_value:,.2f} and ${max_value:,.2f}:[/bold]")
        
        if filtered_trades:
            table = Table(box=box.ROUNDED)
            table.add_column("Timestamp", style="blue")
            table.add_column("Action", style="green")
            table.add_column("Token", style="cyan")
            table.add_column("Amount", style="yellow")
            table.add_column("Value", style="magenta")
            
            for trade in filtered_trades:
                value = trade["amount"] * trade["price"]
                action_style = "green" if trade["action"] == "BUY" else "red" if trade["action"] == "SELL" else "blue"
                table.add_row(
                    trade["timestamp"],
                    f"[{action_style}]{trade['action']}[/{action_style}]",
                    trade["token"],
                    str(trade["amount"]),
                    f"${value:,.2f}"
                )
            
            self.console.print(table)
            self.console.print(f"\n[dim]Found {len(filtered_trades)} matching trades.[/dim]")
        else:
            self.console.print(f"[yellow]No trades found in this value range.[/yellow]")
    
    def _view_decision_history(self):
        """View decision history"""
        self.console.clear()
        
        # Mock decision history data
        decisions = [
            {
                "timestamp": "2024-01-07 12:00:00",
                "type": "Trade Decision",
                "reasoning": "Market analysis shows bullish momentum on ETH with RSI indicating oversold conditions. MACD crossover confirms upward trend.",
                "confidence": 0.85,
                "outcome": "Executed - BUY 100 ETH @ $2,500"
            },
            {
                "timestamp": "2024-01-07 11:45:00",
                "type": "Risk Assessment",
                "reasoning": "Portfolio exposure to BTC exceeds recommended 40% threshold. Partial rebalancing recommended to reduce concentration risk.",
                "confidence": 0.92,
                "outcome": "Executed - SELL 0.5 BTC @ $45,000"
            },
            {
                "timestamp": "2024-01-07 11:30:00",
                "type": "Strategy Analysis",
                "reasoning": "Current market volatility suggests switching to conservative allocation. Reduce high-risk positions and increase stablecoin holdings.",
                "confidence": 0.78,
                "outcome": "Position adjusted - Stablecoin ratio increased to 30%"
            }
        ]
        
        title = Text.from_markup(
            "[bold blue]Decision History[/bold blue]",
            justify="center"
        )
        
        if not decisions:
            info_text = Text.from_markup(
                "\n[yellow]No decision history found.[/yellow]\n\n"
                "[dim]Agent decisions will appear here as they are made during sessions.[/dim]",
                justify="left"
            )
        else:
            # Create decisions table
            table = Table(title="Agent Decision Log", box=box.ROUNDED)
            table.add_column("Timestamp", style="blue")
            table.add_column("Type", style="green")
            table.add_column("Confidence", style="yellow")
            table.add_column("Outcome", style="cyan")
            
            for decision in decisions:
                confidence_color = "green" if decision["confidence"] > 0.8 else "yellow" if decision["confidence"] > 0.6 else "red"
                table.add_row(
                    decision["timestamp"],
                    decision["type"],
                    f"[{confidence_color}]{decision['confidence']:.0%}[/{confidence_color}]",
                    decision["outcome"]
                )
            
            self.console.print(table)
            
            # Show summary
            total_decisions = len(decisions)
            avg_confidence = sum(d["confidence"] for d in decisions) / total_decisions
            
            info_text = Text.from_markup(
                f"\n[bold]Decision Summary:[/bold]\n"
                f"Total Decisions: [cyan]{total_decisions}[/cyan]\n"
                f"Average Confidence: [yellow]{avg_confidence:.0%}[/yellow]\n"
                f"Time Period: [blue]Last 24 hours[/blue]\n\n"
                f"[dim]Decisions are logged with AI reasoning and confidence scores.[/dim]",
                justify="left"
            )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        # Offer to view details if decisions exist
        if decisions:
            if Confirm.ask("\n[bold]View detailed reasoning for a decision?[/bold]"):
                self._view_decision_details(decisions)
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _view_decision_details(self, decisions):
        """View detailed reasoning for a specific decision"""
        self.console.clear()
        
        # Show decisions for selection
        table = Table(title="Select decision for details", box=box.ROUNDED)
        table.add_column("Number", style="cyan", width=8)
        table.add_column("Timestamp", style="blue")
        table.add_column("Type", style="green")
        table.add_column("Confidence", style="yellow")
        
        for i, decision in enumerate(decisions, 1):
            confidence_color = "green" if decision["confidence"] > 0.8 else "yellow" if decision["confidence"] > 0.6 else "red"
            table.add_row(
                str(i),
                decision["timestamp"],
                decision["type"],
                f"[{confidence_color}]{decision['confidence']:.0%}[/{confidence_color}]"
            )
        
        self.console.print(table)
        
        try:
            choice = int(Prompt.ask("Enter decision number for details")) - 1
            if 0 <= choice < len(decisions):
                decision = decisions[choice]
                
                # Detailed decision information
                self.console.print(f"\n[bold]Decision Details:[/bold]")
                self.console.print(f"Timestamp: [blue]{decision['timestamp']}[/blue]")
                self.console.print(f"Type: [green]{decision['type']}[/green]")
                
                confidence_color = "green" if decision["confidence"] > 0.8 else "yellow" if decision["confidence"] > 0.6 else "red"
                self.console.print(f"Confidence: [{confidence_color}]{decision['confidence']:.0%}[/{confidence_color}]")
                self.console.print(f"Outcome: [cyan]{decision['outcome']}[/cyan]")
                
                self.console.print(f"\n[bold]AI Reasoning:[/bold]")
                self.console.print(f"[dim]{decision['reasoning']}[/dim]")
                
                # Mock additional context
                self.console.print(f"\n[bold]Market Context:[/bold]")
                self.console.print(f"[dim]ETH Price: $2,500 (+2.3% 24h)[/dim]")
                self.console.print(f"[dim]BTC Price: $45,000 (-0.8% 24h)[/dim]")
                self.console.print(f"[dim]Market Sentiment: Bullish (Fear & Greed Index: 65)[/dim]")
                
                self.console.print(f"\n[bold]Agent State:[/bold]")
                self.console.print(f"[dim]Model: GPT-4 with market data integration[/dim]")
                self.console.print(f"[dim]Data Sources: Real-time prices, technical indicators, news sentiment[/dim]")
                self.console.print(f"[dim]Strategy: Balanced risk with momentum focus[/dim]")
                
            else:
                self.console.print("[red]Invalid decision number.[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number.[/red]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _export_logs(self):
        """Export logs to file"""
        self.console.clear()
        
        title = Text.from_markup(
            "[bold blue]Export Logs[/bold blue]",
            justify="center"
        )
        
        info_text = Text.from_markup(
            "\n[bold]Export Options:[/bold]\n"
            "❯ [bold green]Export recent trades[/bold green]\n"
            "  [bold green]Export decision history[/bold green]\n"
            "  [bold green]Export all logs[/bold green]\n"
            "  [bold yellow]Back[/bold yellow]",
            justify="left"
        )
        
        panel = Panel(
            Align.center(info_text),
            title=Align.center(title),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        
        export_type = Prompt.ask(
            "\n[bold]Select export type[/bold]",
            choices=["1", "2", "3", "4", "trades", "decisions", "all", "back"],
            default=None
        )
        
        if export_type in ["4", "back"]:
            return
        
        # Get export format
        format_type = Prompt.ask(
            "Select export format",
            choices=["JSON", "CSV", "TXT"],
            default="JSON"
        )
        
        # Get filename
        filename = Prompt.ask("Enter filename (without extension)", default="tradearena_logs")
        
        # Mock export process
        self.console.print(f"\n[bold green]Exporting logs...[/bold green]")
        
        if export_type in ["1", "trades"]:
            trades = self.mock_services.get_agent_logs()
            count = len(trades)
            data_type = "recent trades"
        elif export_type in ["2", "decisions"]:
            count = 3  # Mock count
            data_type = "decision history"
        else:  # all
            count = 6  # Mock count
            data_type = "all logs"
        
        self.console.print(f"[green]✓ Exported {count} {data_type} to {filename}.{format_type.lower()}[/green]")
        self.console.print(f"[dim]File size: ~{count * 2.5}KB[/dim]")
        self.console.print(f"[dim]Location: ./exports/{filename}.{format_type.lower()}[/dim]")
        
        self.console.print("\nPress Enter to continue...")
        input()
    
    def _export_trades(self, trades):
        """Export specific trades"""
        self.console.clear()
        
        format_type = Prompt.ask(
            "Select export format",
            choices=["JSON", "CSV"],
            default="CSV"
        )
        
        filename = Prompt.ask("Enter filename (without extension)", default="trades_export")
        
        self.console.print(f"\n[bold green]Exporting {len(trades)} trades...[/bold green]")
        self.console.print(f"[green]✓ Exported to {filename}.{format_type.lower()}[/green]")
        
        self.console.print("\nPress Enter to continue...")
        input()